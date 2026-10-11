# Experimental v17 subtitle selector

The opt-in `kotoba_capture.selector` module selects reviewable text from existing native OCR arrays using an explicitly configured geometry/style policy. It is not a video runner, an OCR engine, an automatic region detector or a universal subtitle-intent classifier. The original FFmpeg/Tesseract CLI is unchanged.

## Quick checks

From `apps/server`:

```sh
PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests/selector_v17 -t tests -v
/usr/bin/python3 -B -S tests/check_selector_stdlib.py
```

The 116 tests use English synthetic text, geometry and evidence. No model, image, video, private profile, transcript or run is required. The import guard rejects NumPy, OpenCV and PaddleOCR imports. Core bytes are preserved from the frozen v17 experiment; historical `select_caption_profile_v6` remains an alias, not a different engine.

## Synthetic API example

Run this example with `PYTHONPATH=. /usr/bin/python3 -B -S` from `apps/server`. Its fabricated style evidence demonstrates the contract only, not real image measurement. The optional image adapter is available through a separate opt-in module; the experimental complete-video runner remains follow-up work. This core example does not import either.

```python
import hashlib
import json
from kotoba_capture.selector import select_caption_profile_v17

def binding(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False,
        sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

poly = [[200, 150], [800, 150], [800, 210], [200, 210]]
native = dict(rec_texts=['Main caption 2'], rec_scores=[0.9],
    rec_boxes=[[200, 150, 800, 210]], dt_polys=[poly], rec_polys=[poly])
geometry = dict(sourceWidth=1000, sourceHeight=1000, crop=[0, 0, 1000, 1000])
policy = dict(roi=[0, 0, 1, 1], mainHeight=[0.04, 0.08],
    rowCenterTolerance=0.015, maxInlineGap=0.05, maxRowGap=0.06,
    minHorizontalOverlap=0.2, minConfidence=0, maxRows=8,
    maxHorizontalTiltDegrees=3,
    background='no_constraint', orientation='horizontal',
    styleRequired=True, requiredVisualStyle='light_fill_dark_outline',
    minimumAnchorAspectRatio=3, auxiliaryHeightRatio=0.8)
identity = hashlib.sha256(b'Synthetic image identity, not real pixels').hexdigest()
# Toy contract demonstration ONLY. For real images obtain measurements from
# the optional adapter, not invented statuses or reference-derived labels.
evidence = dict(schema='caption-style-evidence/v1',
    adapterVersion='light-outline-components-v2', style='light_fill_dark_outline',
    imageSha256=identity, nativeSha256=binding(native),
    geometrySha256=binding(geometry),
    entries=[dict(index=0, status='match', reason='Synthetic demonstration only')])
result = select_caption_profile_v17(dict(width=1000, height=1000), native,
    policy, geometry, style_evidence=evidence, expected_image_sha256=identity)
assert result['text'] == 'Main caption 2'
assert result['nativeResult'] == native
assert result['reviewRequired'] is True
```

## Contract and manual configuration

`select_caption_profile_v17(image, native_result, policy, frame_geometry, *, blue_panel_evidence=None, style_evidence=None, expected_image_sha256=None)` returns selected text, original native arrays, indices, exclusions and review flags. The five native arrays retain original indices and characters; no missing character is invented or repaired. Crop-local OCR coordinates are transformed using source dimensions and crop geometry.

ROI, font-height bands, aspect ratios, row gaps and optional horizontal tilt are manual priors, not universal defaults. The example's full viewport and eight-row maximum are demonstration settings only. `styleRequired=True` requires matching image/native/geometry/index bindings; missing or stale evidence fails closed. `styleRequired=False` explicitly selects the legacy geometry-only mode; never silently downgrade a required-style policy. A `blue_panel` policy also requires caller-supplied region evidence.

| Evidence | Meaning |
|---|---|
| Match | May anchor typography exclusions and main-row grouping. |
| Mismatch | Audited style exclusion before main admission. |
| Unknown | Not a Match. Independent conservative geometry may exclude it; plausible main/crossing/group conflicts retain review. |

Multiple plausible groups and clipped continuations can cause abstention. Geometric auxiliary exclusions do not prove furigana extraction. `reviewRequired=True` remains true even for selected output; OCR confidence and visual features are uncalibrated heuristics. Empty output or abstention is not proof of a subtitle-free frame.

## Evidence limits and next step

Frozen within-source evaluation covered 18 isolated positive images from three known videos: 17 exact outputs, one character edit among 436 reference characters (about 0.23%), and no complete omission. A later provisional negative evaluation produced one false positive among 18 negative scenes: a promotional text box. Matching pixel style does not prove speech-subtitle intent.

These small, correlated, assistant-adjudicated samples are not human-confirmed ground truth, unseen-positive generalization, continuous subtitle coverage or complete-video evidence. Do not interpret character accuracy as detection recall. Sampling times are approximate display times, not audio alignment.

This commit preserves experimental code; it does not certify product readiness. Next: build a reproducible local full-video pilot using the separately preserved optional visual adapter without retuning the frozen selector during evaluation. Keep all media, models, snapshots, OCR text, references and detailed reports under ignored `.local/`; only code, synthetic tests and aggregate metrics belong in Git.

## Optional visual adapter

Import `kotoba_capture.style_evidence` explicitly with an interpreter that already has NumPy and OpenCV. This preserved module is not imported by the selector, package initializer or default Tesseract CLI. No OCR engine, model, installation or source-specific profile is included.

- `measure(rgb, polygon)` measures a crop-local four-point polygon.
- `from_rgb(rgb, native, geometry, image_sha)` accepts RGB `uint8` arrays shaped `(crop_height, crop_width, 3)` and returns indexed evidence for all recognition polygons.
- `from_path(path, native, geometry)` decodes an encoded image with OpenCV, converts BGR to RGB and hashes the exact file bytes.

For in-memory callers, the supplied identity must match the selector's expected image identity; `from_rgb` cannot verify that the caller's hash actually describes those pixels. The complete native result and geometry are separately bound using sorted compact JSON. Do not filter native arrays or fabricate statuses from reference text. Measurements describe physical style, not semantic subtitle intent or calibrated probability.

Run the nine synthetic pixel tests from `apps/server`, using an interpreter with the existing optional dependencies:

```sh
PYTHONPATH=. python -B -m unittest discover -s tests/selector_style -t tests -v
```

Dependency-free full-suite execution skips these nine tests only when NumPy or OpenCV cannot be found. If dependencies are present but broken, or the adapter API fails, the tests fail rather than skip. The 116-test selector guard remains separately dependency-free. Synthetic pixel tests create arrays in memory; no image asset or OCR run is tracked.

The following example runs only with those optional dependencies:

```python
import hashlib
import numpy as np
from kotoba_capture.style_evidence import from_rgb

rgb = np.zeros((80, 200, 3), dtype=np.uint8)
poly = [[10, 10], [180, 10], [180, 60], [10, 60]]
native = dict(rec_texts=['Toy caption'], rec_scores=[0.9],
    rec_boxes=[[10, 10, 180, 60]], rec_polys=[poly], dt_polys=[poly])
geometry = dict(sourceWidth=200, sourceHeight=80, crop=[0, 0, 200, 80])
identity = hashlib.sha256(b'Synthetic encoded-image identity').hexdigest()
evidence = from_rgb(rgb, native, geometry, identity)
assert evidence['entries'][0]['status'] == 'mismatch'
```
