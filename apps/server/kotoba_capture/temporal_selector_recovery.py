"""Review-only proposals from immutable, already-validated v17 record payloads."""
from copy import deepcopy
import hashlib
import json
import math
import re
import unicodedata

from .selector import _valid_style_evidence, select_caption_profile_v17

PROFILE = "temporal-review/v1"
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SOURCE_KEYS = ("videoSha256", "runSha256", "nativeProvenanceSha256",
                "styleProvenanceSha256", "modelProvenanceSha256")


def _finite(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _hash(value):
    return isinstance(value, str) and _SHA256.fullmatch(value) is not None


def _canonical_hash(value):
    try:
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError):
        return None
    return hashlib.sha256(raw).hexdigest()


def _normalize(value):
    return " ".join(unicodedata.normalize("NFKC", value).split()) if isinstance(value, str) else None


def _frozen_valid(frozen):
    if not isinstance(frozen, dict) or not isinstance(frozen.get("policy"), dict):
        return False
    source = frozen.get("source")
    return (isinstance(source, dict) and source.get("profile") == "roi-guided-v17"
            and all(_hash(source.get(key)) for key in _SOURCE_KEYS))


def _record_valid(slot, frozen):
    if not isinstance(slot, dict) or not _finite(slot.get("timestampSeconds")) or slot["timestampSeconds"] < 0:
        return None
    if slot.get("source") != frozen["source"]:
        return None
    record = slot.get("record")
    if not isinstance(record, dict) or record.get("schema") != "kotoba-video-pilot/v1":
        return None
    if (not isinstance(record.get("index"), int) or not _finite(record.get("timestamp"))
            or record["timestamp"] != slot["timestampSeconds"] or not _hash(record.get("identitySha256"))
            or not _hash(record.get("imageSha256")) or not _hash(record.get("recordSha256"))):
        return None
    candidate = {key: value for key, value in record.items() if key != "recordSha256"}
    if _canonical_hash(candidate) != record["recordSha256"]:
        return None
    geometry, native, style, selected = (record.get("frameGeometry"), record.get("nativeResult"),
                                         record.get("styleEvidence"), record.get("selected"))
    if not isinstance(geometry, dict) or not isinstance(native, dict) or not isinstance(style, dict) or not isinstance(selected, dict):
        return None
    try:
        crop = geometry["crop"]
        if not isinstance(crop, list) or len(crop) != 4 or any(not _finite(value) for value in crop):
            return None
        image = {"width": crop[2], "height": crop[3]}
        if not _valid_style_evidence(style, record["imageSha256"], native, geometry, "light_fill_dark_outline"):
            return None
        replayed = select_caption_profile_v17(image, native, frozen["policy"], geometry,
                                               style_evidence=style, expected_image_sha256=record["imageSha256"])
    except (KeyError, TypeError, ValueError, OverflowError):
        return None
    return record if replayed == selected else None


def _bounds(value):
    if not isinstance(value, list) or len(value) != 4 or any(not _finite(v) for v in value):
        return None
    x1, y1, x2, y2 = value
    return value if 0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1 else None


def _iou(left, right):
    ix1, iy1, ix2, iy2 = max(left[0], right[0]), max(left[1], right[1]), min(left[2], right[2]), min(left[3], right[3])
    overlap = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    union = (left[2] - left[0]) * (left[3] - left[1]) + (right[2] - right[0]) * (right[3] - right[1]) - overlap
    return overlap / union if union > 0 else 0


def _group(record, rows, group_id, *, require_style_match=True):
    native, style = record["nativeResult"], record["styleEvidence"]
    texts = native.get("rec_texts")
    statuses = {entry.get("index"): entry.get("status") for entry in style.get("entries", []) if isinstance(entry, dict)}
    if not isinstance(rows, list) or not rows or not isinstance(texts, list):
        return None
    seen, normalized_rows, raw_rows, boxes = set(), [], [], []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("indices"), list) or not row["indices"]:
            return None
        indices, row_text, box = row["indices"], row.get("text"), _bounds(row.get("bounds"))
        if box is None or not isinstance(row_text, str) or not _normalize(row_text):
            return None
        if any(type(index) is not int or index in seen or not 0 <= index < len(texts) for index in indices):
            return None
        if any(not isinstance(texts[index], str) for index in indices):
            return None
        if require_style_match and any(statuses.get(index) != "match" for index in indices):
            return None
        native_text = "".join(texts[index] for index in indices)
        if native_text != row_text:
            return None
        seen.update(indices); normalized_rows.append(_normalize(row_text)); raw_rows.append(row_text); boxes.append(box)
    aggregate = [min(box[0] for box in boxes), min(box[1] for box in boxes),
                 max(box[2] for box in boxes), max(box[3] for box in boxes)]
    return {"groupId": group_id, "text": "\n".join(raw_rows), "normalizedText": "\n".join(normalized_rows),
            "rows": deepcopy(rows), "bounds": aggregate}


def _candidate_groups(record):
    selected = record["selected"]
    groups = selected.get("candidateGroups")
    if not selected.get("roiCovered") or not isinstance(groups, list):
        return None
    result = []
    for index, group in enumerate(groups):
        if not isinstance(group, list):
            return None
        parsed = _group(record, group, index, require_style_match=False)
        if parsed is None:
            return None
        parsed["styleQualified"] = _group(record, group, index, require_style_match=True) is not None
        result.append(parsed)
    return result


def _selected_anchor(record):
    selected = record["selected"]
    if selected.get("status") != "selected" or selected.get("reason") != "unique_roi_typography_group":
        return None
    return _group(record, selected.get("rows"), 0)


def _output(baseline, radius_seconds, attempt_budget):
    selected = baseline.get("record", {}).get("selected") if isinstance(baseline, dict) else None
    return {"profile": PROFILE, "baseline": deepcopy(baseline), "result": deepcopy(selected), "proposal": None,
            "reason": "review_needed", "reviewRequired": True, "continuityVerified": False,
            "captionIntentVerified": False,
            "audit": {"radiusSeconds": radius_seconds, "attemptBudget": attempt_budget,
                      "attemptsUsed": 0, "attempts": [], "outsideWindow": [], "budgetExhausted": False,
                      "competitorGroups": []}}


def propose_temporal_review(baseline, slots, *, frozen, radius_seconds=2.0, attempt_budget=8, minimum_iou=.85):
    """Return an immutable v17 baseline plus at most one explicitly review-only proposal.

    The caller validates stored pilot records and original frame bytes against the stored
    plan before constructing slots. This pure helper rechecks canonical record/style/
    selector bindings; it neither resumes a pilot nor reads images, models, or references.
    """
    output = _output(baseline, radius_seconds, attempt_budget)
    if (not _finite(radius_seconds) or not 0 < radius_seconds <= 2 or type(attempt_budget) is not int
            or not 1 <= attempt_budget <= 8 or not _finite(minimum_iou) or minimum_iou != .85):
        output["reason"] = "invalid_config"
        return output
    if not _frozen_valid(frozen):
        output["reason"] = "invalid_frozen_identity"
        return output
    current = _record_valid(baseline, frozen)
    if current is None:
        output["reason"] = "invalid_current_record"
        return output
    if current["selected"].get("status") == "selected":
        output["reason"] = "baseline_selected_preserved"
        return output
    if current["selected"].get("reason") not in ("ambiguous_groups", "unknown_visual_style"):
        output["reason"] = "unsupported_abstention"
        return output
    groups = _candidate_groups(current)
    if groups is None:
        output["reason"] = "invalid_current_groups"
        return output
    output["audit"]["competitorGroups"] = deepcopy(groups)
    if not isinstance(slots, list):
        output["reason"] = "invalid_slot_pool"
        return output
    center, previous, ranked = baseline["timestampSeconds"], None, []
    for slot in slots:
        timestamp = slot.get("timestampSeconds") if isinstance(slot, dict) else None
        if not _finite(timestamp) or timestamp < 0 or timestamp == center or (previous is not None and timestamp <= previous):
            output["reason"] = "invalid_slot_placement"
            return output
        previous = timestamp
        if abs(timestamp - center) > radius_seconds:
            output["audit"]["outsideWindow"].append(timestamp)
        else:
            ranked.append((abs(timestamp - center), timestamp, slot))
    ranked.sort(key=lambda item: (item[0], item[1]))
    blocked = {-1: False, 1: False}
    for _, timestamp, slot in ranked[:attempt_budget]:
        direction = -1 if timestamp < center else 1
        attempt = {"timestampSeconds": timestamp, "offsetSeconds": timestamp - center}
        output["audit"]["attempts"].append(attempt); output["audit"]["attemptsUsed"] += 1
        if blocked[direction]:
            attempt["reason"] = "blocked_by_changed_caption"
            continue
        neighbor = _record_valid(slot, frozen)
        if neighbor is None:
            attempt["reason"] = "unknown_slot"
            continue
        anchor = _selected_anchor(neighbor)
        if anchor is None:
            attempt["reason"] = "ineligible_neighbor"
            continue
        matching = [group for group in groups if group["styleQualified"] and group["normalizedText"] == anchor["normalizedText"]]
        if not matching:
            attempt["reason"] = "changed_caption_boundary"; blocked[direction] = True
            continue
        if len(matching) != 1:
            attempt["reason"] = "ambiguous_matching_groups"
            output["reason"] = "ambiguous_matching_groups"
            return output
        group = matching[0]
        geometry = _iou(group["bounds"], anchor["bounds"])
        if geometry < minimum_iou:
            attempt["reason"] = "geometry_mismatch"
            continue
        attempt.update(reason="matching_anchor_proposed", anchorId=neighbor["index"], groupId=group["groupId"], boxIou=geometry)
        output["proposal"] = {"text": group["text"], "groupId": group["groupId"], "rows": deepcopy(group["rows"]),
                              "anchorId": neighbor["index"], "anchorTimestampSeconds": timestamp,
                              "boxIou": geometry, "source": deepcopy(frozen["source"])}
        output["reason"] = "matching_neighbor_requires_review"
        return output
    output["audit"]["budgetExhausted"] = len(ranked) > output["audit"]["attemptsUsed"]
    output["reason"] = "no_safe_proposal"
    return output
