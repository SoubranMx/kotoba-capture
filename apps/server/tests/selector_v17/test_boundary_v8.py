from .test_selector import selector,policy,native,image,geometry
import unittest
class BoundaryV8Tests(unittest.TestCase):
 def select(self,*boxes):return selector.select_caption_profile_v17(image(),native(*boxes),policy(),geometry())
 def test_far_left(self):
  r=self.select(('Caption',[500,150,800,210]),('Large notice',[0,110,300,250]));self.assertEqual(r['text'],'Caption');self.assertIn({'index':1,'reason':'boundary_crossing_unaffiliated'},r['rejected'])
 def test_far_right(self):
  self.assertEqual(self.select(('Caption',[200,150,500,210]),('Notice',[700,110,1000,250]))['text'],'Caption')
 def test_gap_thresholds(self):
  for gap in [49,50,51]:
   r=self.select(('Caption',[400,150,800,210]),('Notice',[0,110,400-gap,250]))
   self.assertEqual(r['status'],'selected' if gap>50 else 'review')
 def test_no_anchor(self):self.assertEqual(self.select(('Notice',[0,110,300,250]))['status'],'review')
 def test_overlapping(self):self.assertEqual(self.select(('Caption',[200,150,800,210]),('Notice',[0,110,500,250]))['status'],'review')
 def test_any_anchor_close(self):self.assertEqual(self.select(('Far caption',[600,150,850,210]),('Near caption',[200,230,450,290]),('Notice',[0,170,160,310]))['status'],'review')
