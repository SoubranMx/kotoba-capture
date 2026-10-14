"""Synthetic contract tests for review-only temporal selector proposals."""
import copy
import hashlib
import json
import math
import unittest

from kotoba_capture.selector import _style_binding, select_caption_profile_v17
from kotoba_capture.temporal_selector_recovery import propose_temporal_review


def binding(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def policy():
    return {
        "roi": [0, 0, 1, 1], "mainHeight": [.04, .2], "rowCenterTolerance": .03,
        "maxInlineGap": .03, "maxRowGap": .1, "minHorizontalOverlap": .1,
        "maxRows": 3, "orientation": "horizontal",
        "styleRequired": True, "requiredVisualStyle": "light_fill_dark_outline",
    }


def native(*entries):
    result = {"rec_texts": [], "rec_scores": [], "rec_boxes": [], "dt_polys": [], "rec_polys": []}
    for text, box in entries:
        x1, y1, x2, y2 = box
        polygon = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        result["rec_texts"].append(text); result["rec_scores"].append(.9)
        result["rec_boxes"].append(box); result["dt_polys"].append(polygon); result["rec_polys"].append(copy.deepcopy(polygon))
    return result


def frozen():
    return {
        "policy": policy(),
        "source": {
            "videoSha256": "a" * 64, "runSha256": "b" * 64,
            "nativeProvenanceSha256": "c" * 64, "styleProvenanceSha256": "d" * 64,
            "modelProvenanceSha256": "e" * 64, "profile": "roi-guided-v17",
        },
    }


def record(index, timestamp, *entries, source=None):
    geometry = {"sourceWidth": 1000, "sourceHeight": 1000, "crop": [0, 0, 1000, 1000]}
    raw = native(*entries)
    image_hash = ("%064x" % (index + 1))[-64:]
    style = {
        "schema": "caption-style-evidence/v1", "style": "light_fill_dark_outline",
        "adapterVersion": "light-outline-components-v2", "imageSha256": image_hash,
        "nativeSha256": _style_binding(raw), "geometrySha256": _style_binding(geometry),
        "entries": [{"index": i, "status": "match", "reason": "synthetic"} for i in range(len(entries))],
    }
    selected = select_caption_profile_v17({"width": 1000, "height": 1000}, raw, policy(), geometry,
                                           style_evidence=style, expected_image_sha256=image_hash)
    value = {"schema": "kotoba-video-pilot/v1", "index": index, "timestamp": timestamp,
             "identitySha256": "f" * 64, "frameGeometry": geometry, "imageSha256": image_hash,
             "nativeResult": raw, "styleEvidence": style, "selected": selected}
    value["recordSha256"] = binding(value)
    return {"timestampSeconds": timestamp, "source": source or frozen()["source"], "record": value}


def rebind(slot):
    value = slot["record"]
    geometry, raw, style = value["frameGeometry"], value["nativeResult"], value["styleEvidence"]
    value["selected"] = select_caption_profile_v17({"width": geometry["crop"][2], "height": geometry["crop"][3]}, raw, policy(), geometry,
                                                       style_evidence=style, expected_image_sha256=value["imageSha256"])
    rehash(slot)


def rehash(slot):
    value = slot["record"]
    value["recordSha256"] = binding({key: item for key, item in value.items() if key != "recordSha256"})


class TemporalSelectorRecoveryTests(unittest.TestCase):
    def proposal_inputs(self):
        current = record(10, 10, ("Anchor", [100, 100, 800, 180]), ("Other", [100, 500, 800, 580]))
        neighbor = record(11, 11, ("Anchor", [100, 100, 800, 180]))
        return current, neighbor

    def test_selected_baseline_passes_through_and_inputs_are_unchanged(self):
        current = record(10, 10, ("Anchor", [100, 100, 800, 180]))
        before = copy.deepcopy(current)
        result = propose_temporal_review(current, None, frozen=frozen())
        self.assertEqual(result["result"], current["record"]["selected"])
        self.assertEqual(result["reason"], "baseline_selected_preserved")
        self.assertEqual(result["audit"]["attemptsUsed"], 0)
        result["result"]["text"] = "changed"
        self.assertEqual(current, before)

    def test_selected_baseline_requires_valid_config_frozen_and_record(self):
        current = record(10, 10, ("Anchor", [100, 100, 800, 180]))
        before = copy.deepcopy(current)
        invalid_cases = [
            (lambda value, state: value["record"].update(recordSha256="0" * 64), frozen(), {}),
            (lambda value, state: value["record"].update(timestamp=math.nan), frozen(), {}),
            (lambda value, state: value.update(source={**value["source"], "videoSha256": "0" * 64}), frozen(), {}),
            (lambda value, state: (value["record"]["selected"].update(text="Changed"), rehash(value)), frozen(), {}),
            (lambda value, state: None, {}, {}),
            (lambda value, state: None, frozen(), {"radius_seconds": math.nan}),
            (lambda value, state: None, frozen(), {"attempt_budget": 0}),
            (lambda value, state: None, frozen(), {"minimum_iou": math.nan}),
        ]
        for mutate, frozen_input, options in invalid_cases:
            with self.subTest(options=options, frozen=frozen_input):
                changed = copy.deepcopy(current)
                mutate(changed, options)
                result = propose_temporal_review(changed, [], frozen=frozen_input, **options)
                self.assertNotEqual(result["reason"], "baseline_selected_preserved")
                self.assertIsNone(result["proposal"])
                self.assertTrue(result["reviewRequired"])
                self.assertEqual(result["baseline"], changed)
        self.assertEqual(current, before)

    def test_selected_baseline_huge_or_non_json_values_fail_closed_without_raising(self):
        current = record(10, 10, ("Anchor", [100, 100, 800, 180]))
        huge = 10 ** 10000
        for mutate in (
            lambda value: value["record"].update(timestamp=huge),
            lambda value: value["record"].update(extra=object()),
        ):
            with self.subTest(mutate=mutate):
                changed = copy.deepcopy(current); mutate(changed)
                result = propose_temporal_review(changed, [], frozen=frozen())
                self.assertEqual(result["reason"], "invalid_current_record")
                self.assertIsNone(result["proposal"])

    def test_unique_matching_current_group_is_review_only_current_raw_text(self):
        current, neighbor = self.proposal_inputs()
        result = propose_temporal_review(current, [neighbor], frozen=frozen())
        self.assertEqual(result["reason"], "matching_neighbor_requires_review")
        self.assertEqual(result["proposal"]["text"], "Anchor")
        self.assertEqual(result["proposal"]["groupId"], 0)
        self.assertEqual(result["proposal"]["anchorId"], 11)
        self.assertTrue(result["reviewRequired"])
        self.assertFalse(result["continuityVerified"])
        self.assertFalse(result["captionIntentVerified"])
        self.assertEqual(result["result"], current["record"]["selected"])
        self.assertEqual(len(result["audit"]["competitorGroups"]), 2)

    def test_unknown_competitor_is_audited_without_vetoing_qualified_group(self):
        current, neighbor = self.proposal_inputs()
        current["record"]["styleEvidence"]["entries"][1]["status"] = "unknown"
        rebind(current)
        before = copy.deepcopy(current)
        result = propose_temporal_review(current, [neighbor], frozen=frozen())
        self.assertEqual(result["reason"], "matching_neighbor_requires_review")
        self.assertEqual(result["proposal"]["groupId"], 0)
        self.assertEqual(len(result["audit"]["competitorGroups"]), 2)
        self.assertEqual(current, before)

    def test_unknown_proposed_group_and_duplicate_qualified_matches_abstain(self):
        current, neighbor = self.proposal_inputs()
        current["record"]["styleEvidence"]["entries"][0]["status"] = "unknown"
        rebind(current)
        result = propose_temporal_review(current, [neighbor], frozen=frozen())
        self.assertIsNone(result["proposal"])
        duplicate = record(10, 10, ("Anchor", [100, 100, 800, 180]), ("Anchor", [100, 500, 800, 580]))
        self.assertEqual(propose_temporal_review(duplicate, [neighbor], frozen=frozen())["reason"], "ambiguous_matching_groups")

    def test_window_and_budget_count_unknown_payloads_exactly(self):
        current, neighbor = self.proposal_inputs()
        slots = [{"timestampSeconds": 10.1}, {"timestampSeconds": 10.2}, neighbor]
        result = propose_temporal_review(current, slots, frozen=frozen(), attempt_budget=2)
        self.assertIsNone(result["proposal"])
        self.assertEqual(result["audit"]["attemptsUsed"], 2)
        self.assertTrue(result["audit"]["budgetExhausted"])
        self.assertEqual([item["reason"] for item in result["audit"]["attempts"]], ["unknown_slot", "unknown_slot"])

    def test_changed_caption_blocks_one_direction_before_farther_anchor(self):
        current, neighbor = self.proposal_inputs()
        changed = record(9, 9.5, ("Changed", [100, 100, 800, 180]))
        result = propose_temporal_review(current, [changed, neighbor], frozen=frozen())
        self.assertIsNotNone(result["proposal"])
        self.assertEqual(result["proposal"]["anchorId"], 11)
        self.assertEqual(result["audit"]["attempts"][0]["reason"], "changed_caption_boundary")
        result = propose_temporal_review(current, [record(9, 9, ("Anchor", [100, 100, 800, 180])), changed], frozen=frozen())
        self.assertIsNone(result["proposal"])
        self.assertEqual(result["audit"]["attempts"][1]["reason"], "blocked_by_changed_caption")

    def test_duplicate_matching_group_and_invalid_current_evidence_abstain(self):
        current = record(10, 10, ("Anchor", [100, 100, 800, 180]), ("Anchor", [100, 500, 800, 580]))
        neighbor = record(11, 11, ("Anchor", [100, 100, 800, 180]))
        self.assertEqual(propose_temporal_review(current, [neighbor], frozen=frozen())["reason"], "ambiguous_matching_groups")
        current, neighbor = self.proposal_inputs()
        current["record"]["styleEvidence"]["entries"][0]["status"] = "unknown"
        self.assertEqual(propose_temporal_review(current, [neighbor], frozen=frozen())["reason"], "invalid_current_record")

    def test_wrong_source_hash_style_roi_orientation_or_row_abstain_fail_closed(self):
        current, neighbor = self.proposal_inputs()
        for mutation in (
            lambda value: value.update(source={**value["source"], "videoSha256": "0" * 64}),
            lambda value: value["record"].update(recordSha256="0" * 64),
            lambda value: value["record"]["styleEvidence"]["entries"][0].update(status="unknown"),
            lambda value: value["record"]["frameGeometry"].update(crop=[0, 0, 500, 1000]),
            lambda value: value["record"]["nativeResult"]["dt_polys"].__setitem__(0, [[0, 0], [0, 100], [20, 100], [20, 0]]),
            lambda value: value["record"]["selected"]["candidateGroups"][0][0].update(indices=[], bounds=[], text=""),
        ):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(current); mutation(changed)
                result = propose_temporal_review(changed, [neighbor], frozen=frozen())
                self.assertIsNone(result["proposal"]); self.assertTrue(result["reviewRequired"])

    def test_nonfinite_values_never_raise_or_canonicalize(self):
        current, neighbor = self.proposal_inputs()
        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(value=value):
                changed = copy.deepcopy(current); changed["record"]["timestamp"] = value
                result = propose_temporal_review(changed, [neighbor], frozen=frozen())
                self.assertEqual(result["reason"], "invalid_current_record")


if __name__ == "__main__":
    unittest.main()
