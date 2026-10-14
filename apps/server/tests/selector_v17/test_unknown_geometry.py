from .test_selector import selector,native,image,geometry,policy
from .test_style_contract import evidence
import unittest
class UnknownGeometry(unittest.TestCase):
 def select(self,n,statuses):
  return selector.select_caption_profile_v17(image(),n,policy(requiredVisualStyle='light_fill_dark_outline',minimumAnchorAspectRatio=3,auxiliaryHeightRatio=.8),geometry(),style_evidence=evidence(n,statuses),expected_image_sha256='a'*64)
 def test_unknown_relative_aux_geometry_excluded(self):
  n=native(('Auxiliary',[220,100,380,145]),('Body caption',[200,155,700,225]));r=self.select(n,['unknown','match']);self.assertEqual(r['text'],'Body caption');self.assertIn(dict(index=0,reason='relative_upper_auxiliary_candidate'),r['rejected']);self.assertEqual(r['styleEvidence']['entries'][0]['status'],'unknown')
 def test_unknown_short_offrow_geometry_excluded(self):
  n=native(('Body caption',[300,160,750,230]),('Print',[110,290,190,350]));r=self.select(n,['match','unknown']);self.assertEqual(r['text'],'Body caption');self.assertIn(dict(index=1,reason='unaffiliated_nonrow_typography'),r['rejected'])
 def test_unknown_anchor_cannot_exclude_matching_main(self):
  n=native(('Matching short',[250,150,350,195]),('Uncertain wide',[200,205,800,275]));r=self.select(n,['match','unknown']);self.assertFalse(any(x['index']==0 and x['reason'] in ('relative_upper_auxiliary_candidate','unaffiliated_nonrow_typography') for x in r['rejected']));self.assertEqual(r['status'],'review')
 def test_unknown_eligible_main_retained_review(self):
  n=native(('Uncertain main',[200,150,800,210]));r=self.select(n,['unknown']);self.assertEqual(r['reason'],'unknown_visual_style');self.assertEqual(r['rejected'],[dict(index=0,reason='unknown_visual_style')])
 def test_unknown_qualifying_competing_group_retained(self):
  n=native(('Main',[110,140,400,200]),('Uncertain group',[600,320,890,380]));r=self.select(n,['match','unknown']);self.assertEqual(r['reason'],'ambiguous_groups')
 def test_unknown_qualifying_crossing_retained(self):
  n=native(('Main',[200,150,800,210]),('Uncertain continuation',[200,390,800,510]));r=self.select(n,['match','unknown']);self.assertEqual(r['reason'],'boundary_crossing_candidate')
