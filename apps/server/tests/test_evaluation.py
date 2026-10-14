import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from kotoba_capture.core import Observation
from kotoba_capture.evaluation import (
    PROVISIONAL_CER_THRESHOLD,
    ReferenceData,
    ReferenceWindow,
    evaluate_reference,
    main,
    levenshtein_edits,
    normalize_evaluation_text,
    parse_reference_markdown,
)


class ReferenceParsingTests(unittest.TestCase):
    def test_reads_only_transcription_and_timestamp_columns(self):
        markdown = """| Japanese Transcription | Translation | Timestamp | Vocabulary |
| --- | --- | --- | --- |
| ｶﾞ です | ignored translation | 00:00 - 00:02 | ignored word |
| 反復 | ignored translation | 00:02 - 00:04 | ignored word |
| untimed row | ignored translation | | ignored word |
| outside | ignored translation | 00:04 - 00:05 | ignored word |
| 今\\|回 | ignored translation | 00:05 - 00:06 | ignored word |
"""

        parsed = parse_reference_markdown(markdown, start=0, end=4)

        self.assertEqual([(row.start, row.end, row.text) for row in parsed.windows], [
            (0.0, 2.0, "ｶﾞ です"),
            (2.0, 4.0, "反復"),
        ])
        self.assertEqual(parsed.untimed_rows_skipped, 1)
        self.assertEqual(parsed.outside_interval_rows_skipped, 2)

    def test_rejects_malformed_populated_timestamps_and_unordered_rows(self):
        malformed = "| Japanese Transcription | Timestamp |\n| --- | --- |\n| text | later-ish |\n"
        unordered = "| Japanese Transcription | Timestamp |\n| --- | --- |\n| second | 00:02 - 00:03 |\n| first | 00:00 - 00:01 |\n"
        for markdown in (malformed, unordered):
            with self.subTest(markdown=markdown), self.assertRaises(ValueError):
                parse_reference_markdown(markdown)

    def test_rejects_empty_or_unusable_reference_and_empty_timestamped_text(self):
        for markdown in (
            "",
            "| Japanese Transcription | Timestamp |\n| --- | --- |\n| untimed | |\n",
            "| Japanese Transcription | Timestamp |\n| --- | --- |\n| | 00:00 - 00:01 |\n",
        ):
            with self.subTest(markdown=markdown), self.assertRaises(ValueError):
                parse_reference_markdown(markdown)

    def test_normalization_preserves_punctuation_and_distance_allows_insertions(self):
        self.assertEqual(normalize_evaluation_text("  ｶﾞ\n,!。 "), "ガ,!。")
        self.assertEqual(levenshtein_edits("猫", "猫AB"), 2)
        self.assertEqual(levenshtein_edits("", "ABC"), 3)


class EvaluationTests(unittest.TestCase):
    def test_modal_selection_ties_missing_windows_repetitions_and_insertion_heavy_cer(self):
        reference = ReferenceData(
            windows=(
                ReferenceWindow(0.0, 2.0, "猫", 1),
                ReferenceWindow(2.0, 4.0, "犬", 2),
                ReferenceWindow(4.0, 6.0, "猫", 3),
            ),
            rows_seen=3,
            untimed_rows_skipped=0,
            outside_interval_rows_skipped=0,
        )
        observations = [
            Observation(0.5, "猫"),
            Observation(1.0, "  "),
            Observation(2.2, "犬AB"),
            Observation(2.4, "犬AB"),
            Observation(6.0, "outside"),
        ]

        result = evaluate_reference(reference, observations, segment_count=4)
        summary = result["summary"]

        self.assertEqual(result["windows"][0]["modal_ocr_text"], "猫")
        self.assertEqual(result["windows"][0]["cer"], 0.0)
        self.assertEqual(result["windows"][1]["cer"], 2.0)
        self.assertTrue(result["windows"][2]["missing_sample_window"])
        self.assertEqual(summary["reference_window_count"], 3)
        self.assertEqual(summary["missing_sample_windows"], 1)
        self.assertEqual(summary["blank_modal_windows"], 0)
        self.assertEqual(summary["exact_match_windows"], 1)
        self.assertEqual(summary["samples_unassigned_to_reference_windows"], 1)
        self.assertEqual(summary["segment_count"], 4)
        self.assertEqual(summary["corpus_edits"], 3)
        self.assertEqual(summary["corpus_reference_characters"], 3)
        self.assertEqual(summary["corpus_cer"], 1.0)
        self.assertEqual(summary["windows_at_or_below_threshold"], 1)
        self.assertEqual(summary["provisional_cer_threshold"], PROVISIONAL_CER_THRESHOLD)

    def test_blank_modal_windows_and_observation_order_validation(self):
        reference = ReferenceData((ReferenceWindow(0.0, 1.0, "確認", 1),), 1, 0, 0)
        result = evaluate_reference(reference, [Observation(0.2, ""), Observation(0.5, "  ")], segment_count=0)
        self.assertEqual(result["summary"]["blank_modal_windows"], 1)
        self.assertEqual(result["summary"]["missing_sample_windows"], 0)
        with self.assertRaises(ValueError):
            evaluate_reference(reference, [Observation(0.5, "x"), Observation(0.4, "y")], segment_count=0)

    def test_cli_writes_private_full_report_but_prints_aggregate_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reference = root / "reference.md"
            reference.write_text(
                "| Japanese Transcription | Timestamp |\n| --- | --- |\n| private cat phrase | 00:00 - 00:01 |\n",
                encoding="utf-8",
            )
            run = root / "run"
            run.mkdir()
            (run / "observations.json").write_text(
                json.dumps({"observations": [{"timestamp": 0.2, "text": "private OCR phrase"}]}),
                encoding="utf-8",
            )
            (run / "segments.json").write_text(json.dumps({"segments": []}), encoding="utf-8")
            output = root / "new evaluation"
            terminal = io.StringIO()

            with redirect_stdout(terminal):
                exit_code = main([
                    "--reference", str(reference),
                    "--run-dir", str(run),
                    "--output-dir", str(output),
                    "--start", "0",
                    "--end", "1",
                ])

            self.assertEqual(exit_code, 0)
            self.assertNotIn("private cat phrase", terminal.getvalue())
            self.assertNotIn("private OCR phrase", terminal.getvalue())
            self.assertEqual(json.loads((output / "evaluation.json").read_text(encoding="utf-8"))["windows"][0]["reference_text"], "private cat phrase")
            self.assertTrue((output / "summary.json").is_file())

    def test_rejects_empty_observations_and_unusable_reference(self):
        reference = ReferenceData((ReferenceWindow(0.0, 1.0, "確認", 1),), 1, 0, 0)
        with self.assertRaises(ValueError):
            evaluate_reference(reference, [], segment_count=0)
        with self.assertRaises(ValueError):
            evaluate_reference(ReferenceData((), 0, 0, 0), [Observation(0.2, "x")], segment_count=0)
        out_of_bounds = ReferenceData((ReferenceWindow(0.0, 2.0, "x", 1),), 1, 0, 0, 0.0, 1.0)
        with self.assertRaises(ValueError):
            evaluate_reference(out_of_bounds, [Observation(0.2, "x")], segment_count=0)
        with self.assertRaises(ValueError):
            parse_reference_markdown("| Japanese Transcription | Timestamp |\n| --- | --- |\n| x | 00:00 - 00:01 |\n", start=1, end=1)


if __name__ == "__main__":
    unittest.main()
