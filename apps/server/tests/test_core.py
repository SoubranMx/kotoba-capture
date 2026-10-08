import json
import unittest

from kotoba_capture.core import (
    Observation,
    group_observations,
    normalize_text,
    segments_to_json,
    segments_to_markdown,
)


class NormalizeTextTests(unittest.TestCase):
    def test_nfkc_and_whitespace_equivalence_preserves_original_observation(self):
        first = Observation(0.0, "ｶﾞ   こんにちは\n世界")
        second = Observation(0.5, "ガ こんにちは 世界")

        self.assertEqual(normalize_text(first.text), normalize_text(second.text))
        segments = group_observations([first, second], sampling_interval=0.5)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].text, first.text)

    def test_groups_only_consecutive_nonempty_equivalent_observations(self):
        observations = [
            Observation(0.0, "A"),
            Observation(0.5, "B"),
            Observation(1.0, "A"),
            Observation(1.5, "   "),
            Observation(2.0, "A"),
        ]

        segments = group_observations(observations, sampling_interval=0.5)

        self.assertEqual([segment.text for segment in segments], ["A", "B", "A", "A"])

    def test_gap_and_optional_end_bound_intervals(self):
        observations = [Observation(1.0, "same"), Observation(1.5, "same"), Observation(3.0, "same")]

        segments = group_observations(observations, sampling_interval=0.5, sample_end=3.2)

        self.assertEqual([(segment.start, segment.end) for segment in segments], [(1.0, 2.0), (3.0, 3.2)])

    def test_decimal_interval_rounding_does_not_split_but_real_extra_gap_does(self):
        observations = [Observation(time, "same") for time in (0.1, 0.2, 0.3, 0.4)]

        segments = group_observations(observations, sampling_interval=0.1, sample_end=0.4)
        larger_gap = group_observations(
            [Observation(0.1, "same"), Observation(0.200001, "same")],
            sampling_interval=0.1,
        )

        self.assertEqual(len(segments), 1)
        self.assertEqual((segments[0].start, segments[0].end), (0.1, 0.4))
        self.assertEqual(len(larger_gap), 2)

    def test_validates_timestamps_interval_and_sample_end(self):
        invalid_cases = [
            ([Observation(float("nan"), "x")], 0.5, None),
            ([Observation(1.0, "x"), Observation(0.0, "y")], 0.5, None),
            ([Observation(0.0, "x")], 0.0, None),
            ([Observation(0.0, "x")], float("inf"), None),
            ([Observation(0.0, "x")], 0.5, -1.0),
        ]
        for observations, interval, sample_end in invalid_cases:
            with self.subTest(observations=observations, interval=interval, sample_end=sample_end):
                with self.assertRaises(ValueError):
                    group_observations(observations, interval, sample_end)

    def test_crop_and_unknown_confidence_are_retained(self):
        observations = [
            Observation(0.0, "字幕", crop_path="frames/first.png"),
            Observation(0.5, "字幕", crop_path="frames/second.png", confidence=0.4),
        ]

        segment = group_observations(observations, 0.5)[0]

        self.assertEqual(segment.crop_path, "frames/first.png")
        self.assertIsNone(segment.confidence)

    def test_crop_sample_is_preferred_over_earlier_confidence_only_sample(self):
        observations = [
            Observation(0.0, "字幕", confidence=0.9),
            Observation(0.5, "字幕", crop_path="frames/second.png"),
        ]

        segment = group_observations(observations, 0.5)[0]

        self.assertEqual(segment.crop_path, "frames/second.png")
        self.assertIsNone(segment.confidence)

    def test_crop_and_confidence_are_selected_as_a_paired_observation(self):
        observations = [
            Observation(0.0, "字幕", confidence=0.9),
            Observation(0.5, "字幕", crop_path="frames/second.png", confidence=0.4),
        ]

        segment = group_observations(observations, 0.5)[0]

        self.assertEqual(segment.crop_path, "frames/second.png")
        self.assertEqual(segment.confidence, 0.4)

    def test_all_no_crop_group_retains_available_confidence(self):
        observations = [Observation(0.0, "字幕"), Observation(0.5, "字幕", confidence=0.4)]

        segment = group_observations(observations, 0.5)[0]

        self.assertIsNone(segment.crop_path)
        self.assertEqual(segment.confidence, 0.4)

    def test_markdown_escapes_angle_brackets_in_multiline_ocr_text(self):
        segment = group_observations([Observation(0.0, "<div\n字幕 <b>text</b>")], 0.5)[0]

        markdown = segments_to_markdown([segment])

        self.assertIn(r"\<div", markdown)
        self.assertIn(r"\<b\>text\</b\>", markdown)
        self.assertIn("字幕", markdown)

    def test_exports_are_unicode_json_and_literal_safe_markdown(self):
        segment = group_observations(
            [Observation(1.0, "字幕 [A]\n二行", crop_path="crops/a (1).png")],
            0.5,
        )[0]

        payload = json.loads(segments_to_json([segment]))
        markdown = segments_to_markdown([segment])

        self.assertEqual(payload["review_status"], "all_text_requires_review")
        self.assertEqual(payload["segments"][0]["text"], "字幕 [A]\n二行")
        self.assertIn(r"字幕 \[A\]", markdown)
        self.assertIn("二行", markdown)
        self.assertIn("crops/a%20%281%29.png", markdown)


if __name__ == "__main__":
    unittest.main()
