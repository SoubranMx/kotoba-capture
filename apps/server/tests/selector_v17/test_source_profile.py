from .test_selector import selector,native,image,geometry,policy
import json,unittest
class SourceProfileTests(unittest.TestCase):
 def configured(self):return policy(roi=[0,.03,1,.45],mainHeight=[.062,.1],rowCenterTolerance=.025,maxRowGap=.07,minimumAnchorAspectRatio=3,auxiliaryHeightRatio=.8)
 def select(self,*boxes):return selector.select_caption_profile_v17(image(),native(*boxes),self.configured(),geometry())
 def test_profile_boundaries(self):
  p=self.configured();self.assertEqual(p['roi'],[0,.03,1,.45]);self.assertEqual(p['mainHeight'],[.062,.1])
 def test_lower_main_is_retained(self):self.assertEqual(self.select(('Body caption',[200,355,800,425]))['text'],'Body caption')
 def test_true_lower_clipping_abstains(self):self.assertEqual(self.select(('Body caption',[200,355,800,425]),('Next caption',[220,410,780,480]))['status'],'review')
 def test_smaller_printed_group_rejected(self):
  r=self.select(('Body caption',[200,100,800,170]),('Printed notice',[110,260,400,310]));self.assertEqual(r['text'],'Body caption');self.assertEqual(r['selectedIndices'],[0])
 def test_competing_main_group_abstains(self):self.assertEqual(self.select(('Body caption',[200,100,800,170]),('Other body',[110,300,400,370]))['status'],'review')
 def test_aligned_digit_prefix_survives(self):self.assertEqual(self.select(('2',[200,355,270,425]),('receipts',[280,355,800,425]))['text'],'2receipts')
