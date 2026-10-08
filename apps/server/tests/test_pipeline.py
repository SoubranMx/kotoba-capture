import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kotoba_capture.pipeline import (
    PipelineError,
    ROI,
    parse_tesseract_tsv,
    run_pipeline,
    validate_roi,
)


VIDEO_PROBE = json.dumps({"streams": [{"width": 1920, "height": 1080}], "format": {"duration": "10.0"}})
TSV = (
    "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
    "5\t1\t1\t1\t1\t1\t0\t0\t10\t10\t80\t字幕\n"
    "5\t1\t1\t1\t1\t2\t10\t0\t10\t10\t60\tです\n"
    "5\t1\t1\t1\t2\t1\t0\t10\t10\t10\t-1\t二行\n"
)


class TsvParsingTests(unittest.TestCase):
    def test_preserves_tesseract_line_order_and_averages_known_confidence(self):
        text, confidence = parse_tesseract_tsv(TSV)

        self.assertEqual(text, "字幕です\n二行")
        self.assertAlmostEqual(confidence, 0.7)

    def test_empty_or_header_only_tsv_keeps_unknown_confidence(self):
        text, confidence = parse_tesseract_tsv(TSV.splitlines()[0] + "\n")

        self.assertEqual(text, "")
        self.assertIsNone(confidence)


class ValidationTests(unittest.TestCase):
    def test_roi_requires_integer_nonnegative_origin_and_in_frame_bounds(self):
        self.assertEqual(validate_roi(ROI(10, 20, 640, 360), 1920, 1080), ROI(10, 20, 640, 360))
        for roi in (ROI(-1, 0, 1, 1), ROI(0, 0, 0, 1), ROI(1900, 0, 21, 1), ROI(0.5, 0, 1, 1)):
            with self.subTest(roi=roi), self.assertRaises(ValueError):
                validate_roi(roi, 1920, 1080)

    def test_run_validates_interval_bounds_and_fresh_output_before_writing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            video = root / "video file.webm"
            video.touch()
            model = root / "tessdata"
            model.mkdir()
            (model / "jpn.traineddata").write_bytes(b"test model")
            output = root / "new output"
            for start, end, interval in ((0, 1, 0), (-1, 1, 0.5), (2, 1, 0.5), (0, 11, 0.5)):
                with self.subTest(start=start, end=end, interval=interval):
                    with patch("kotoba_capture.pipeline.shutil.which", return_value="/usr/bin/tool"), patch(
                        "kotoba_capture.pipeline.subprocess.run", return_value=completed(VIDEO_PROBE)
                    ):
                        with self.assertRaises(ValueError):
                            run_pipeline(video, output, model, start=start, end=end, interval=interval)
                    self.assertFalse(output.exists())


class PipelineIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.video = self.root / "video with spaces.webm"
        self.video.touch()
        self.model = self.root / "model dir"
        self.model.mkdir()
        (self.model / "jpn.traineddata").write_bytes(b"synthetic model bytes")
        self.output = self.root / "run output"

    def test_builds_safe_roi_commands_and_writes_local_observations_and_exports(self):
        calls = []

        def fake_run(command, **kwargs):
            calls.append((command, kwargs))
            if command[0].endswith("ffprobe"):
                return completed(VIDEO_PROBE)
            if command[-1] in ("-version", "--version"):
                return completed("tool version 1")
            if "ffmpeg" in Path(command[0]).name:
                return completed(stdout=b"synthetic png bytes")
            if Path(command[0]).name == "tesseract":
                return completed(TSV, stdin=kwargs.get("input"))
            self.fail(f"unexpected command kind: {command[0]}")

        with patch("kotoba_capture.pipeline.shutil.which", side_effect=lambda name: f"/usr/bin/{name}"), patch(
            "kotoba_capture.pipeline.subprocess.run", side_effect=fake_run
        ):
            summary = run_pipeline(
                self.video,
                self.output,
                self.model,
                start=0,
                end=1.5,
                interval=0.5,
                roi=ROI(1, 1, 5, 5),
            )

        ffmpeg = next(call[0] for call in calls if "-vf" in call[0])
        tesseract = next(call[0] for call in calls if Path(call[0][0]).name == "tesseract" and len(call[0]) > 2)
        self.assertIn("crop=5:5:1:1:exact=1", ffmpeg)
        self.assertIn(str(self.video), ffmpeg)
        self.assertIn("--oem", tesseract)
        self.assertEqual(tesseract[tesseract.index("--oem") + 1], "1")
        self.assertEqual(tesseract[tesseract.index("--psm") + 1], "6")
        self.assertEqual(tesseract[tesseract.index("-c") + 1], "tessedit_create_tsv=1")
        self.assertIn(str(self.model), tesseract)
        self.assertEqual(summary["sample_count"], 3)
        observations = json.loads((self.output / "observations.json").read_text(encoding="utf-8"))
        self.assertEqual(len(observations["observations"]), 3)
        self.assertEqual(observations["observations"][0]["crop_path"], "crops/sample_000001.png")
        self.assertTrue((self.output / "segments.json").is_file())
        self.assertTrue((self.output / "review.md").is_file())
        self.assertEqual((self.output / "crops/sample_000001.png").read_bytes(), b"synthetic png bytes")
        for command, kwargs in calls:
            self.assertIsInstance(command, list)
            self.assertFalse(kwargs.get("shell", False))

    def test_blank_ocr_is_retained_as_an_observation(self):
        responses = iter([
            completed(VIDEO_PROBE),
            completed("tool version 1"),
            completed("tool version 1"),
            completed(stdout=b"png"),
            completed(TSV.splitlines()[0] + "\n"),
        ])
        with patch("kotoba_capture.pipeline.shutil.which", side_effect=lambda name: f"/usr/bin/{name}"), patch(
            "kotoba_capture.pipeline.subprocess.run", side_effect=lambda *args, **kwargs: next(responses)
        ):
            summary = run_pipeline(self.video, self.output, self.model, start=0, end=0.5)
        observations = json.loads((self.output / "observations.json").read_text(encoding="utf-8"))["observations"]
        self.assertEqual(summary["sample_count"], 1)
        self.assertEqual(observations[0]["text"], "")
        self.assertIsNone(observations[0]["confidence"])

    def test_missing_model_dependency_existing_output_and_process_failures_are_clear(self):
        with patch("kotoba_capture.pipeline.shutil.which", side_effect=lambda name: None if name == "tesseract" else "/usr/bin/tool"):
            with self.assertRaisesRegex(PipelineError, "tesseract"):
                run_pipeline(self.video, self.output, self.model, start=0, end=1)
        with patch("kotoba_capture.pipeline.shutil.which", side_effect=lambda name: f"/usr/bin/{name}"), patch(
            "kotoba_capture.pipeline.subprocess.run", return_value=completed(VIDEO_PROBE)
        ):
            with self.assertRaisesRegex(PipelineError, "jpn.traineddata"):
                run_pipeline(self.video, self.output, self.root / "missing model", start=0, end=1)
        self.output.mkdir()
        with patch("kotoba_capture.pipeline.shutil.which", side_effect=lambda name: f"/usr/bin/{name}"):
            with self.assertRaisesRegex(PipelineError, "already exists"):
                run_pipeline(self.video, self.output, self.model, start=0, end=1)
        self.output.rmdir()
        with patch("kotoba_capture.pipeline.shutil.which", side_effect=lambda name: f"/usr/bin/{name}"), patch(
            "kotoba_capture.pipeline.subprocess.run",
            return_value=completed("", "synthetic probe failure", 7),
        ):
            with self.assertRaisesRegex(PipelineError, "ffprobe failed with exit code 7"):
                run_pipeline(self.video, self.output, self.model, start=0, end=1)
        with patch("kotoba_capture.pipeline.shutil.which", side_effect=lambda name: f"/usr/bin/{name}"), patch(
            "kotoba_capture.pipeline.subprocess.run", side_effect=subprocess.TimeoutExpired("ffprobe", 1)
        ):
            with self.assertRaisesRegex(PipelineError, "timed out"):
                run_pipeline(self.video, self.output, self.model, start=0, end=1)
        self.assertFalse(self.output.exists())


def completed(stdout="", stderr="", returncode=0, **kwargs):
    if isinstance(stdout, bytes):
        return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr=stderr)
    return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr=stderr)


if __name__ == "__main__":
    unittest.main()
