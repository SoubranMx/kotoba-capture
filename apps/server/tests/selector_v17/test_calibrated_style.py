from .test_selector import selector,native,image,geometry,policy
import unittest
class CalibratedStyleTests(unittest.TestCase):

    def test_boolean_style_requirement_rejects_wrong_type(self):
        n = native(('Main', [200, 150, 800, 210]))
        r = selector.select_caption_profile_v17(image(), n, policy(styleRequired='false'), geometry())
        self.assertEqual(r['reason'], 'invalid_policy')

    def test_explicit_blue_compatibility_no_evidence_needed(self):
        n = native(('Legacy caption', [200, 150, 800, 210]))
        r = selector.select_caption_profile_v17(image(), n, policy(styleRequired=False), geometry())
        self.assertEqual(r['text'], 'Legacy caption')
