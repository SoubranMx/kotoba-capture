from .test_polygon_orientation import fixture
from .test_selector import selector,image,geometry,policy
from .test_style_contract import evidence
from pathlib import Path
import unittest,json,copy
class RendererPrior(unittest.TestCase):
 def select(self,angle):
  n=fixture(angle,angle);p=policy(roi=[0,0,1,1],mainHeight=[.045,.1],rowCenterTolerance=.025,maxRowGap=.07,maxRows=8,requiredVisualStyle='light_fill_dark_outline',minimumAnchorAspectRatio=3,auxiliaryHeightRatio=.8,maxHorizontalTiltDegrees=3);return selector.select_caption_profile_v17(image(),n,p,geometry(),style_evidence=evidence(n,['match','unknown']),expected_image_sha256='a'*64)
 def test_coherent_rotated_unknown_excluded_configured(self):
  r=self.select(4.8);self.assertEqual(r['text'],'Main caption');self.assertEqual(r['styleEvidence']['entries'][1]['status'],'unknown')
 def test_threshold_equality_is_not_excluded(self):self.assertEqual(self.select(3)['status'],'review')
 def test_nominal_renderer_noise_remains_eligible(self):self.assertEqual(self.select(1.8)['status'],'review')
