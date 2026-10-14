from .test_selector import selector,native,image,geometry,policy
import copy,json,unittest
class LineWidthTests(unittest.TestCase):
 def policy(self):return policy(roi=[0,.03,1,.45],mainHeight=[.045,.1],rowCenterTolerance=.025,maxRowGap=.07,minimumAnchorAspectRatio=5,auxiliaryHeightRatio=.8)
 def select(self,n):return selector.select_caption_profile_v17(image(),n,self.policy(),geometry())
 def test_wide_main_offrow_print(self):
  n=native(('A wide main caption',[100,80,900,150]),('Printed notice',[340,300,660,380]));before=copy.deepcopy(n);r=self.select(n)
  self.assertEqual(r['text'],'A wide main caption');self.assertEqual(r['selectedIndices'],[0]);self.assertEqual(r['nativeResult'],before);self.assertEqual(n,before);self.assertTrue(any(x['index']==1 for x in r['rejected']))
 def test_wide_competitor_still_abstains(self):
  r=self.select(native(('Main',[100,80,900,150]),('Wide competing notice',[200,300,800,380])))
  self.assertEqual(r['reason'],'ambiguous_groups')
 def test_no_anchor_preserves_previous_conservatism(self):
  n=native(('Short main',[350,100,650,170]));p=self.policy();old=copy.deepcopy(p);old['minimumAnchorAspectRatio']=3
  self.assertEqual(self.select(n)['text'],selector.select_caption_profile_v17(image(),n,old,geometry())['text'])
 def test_inline_prefix_and_digit_retained(self):
  r=self.select(native(('Speaker:',[100,90,180,160]),('A wide continuation',[200,90,850,160]),('2',[860,90,935,160])))
  self.assertEqual(r['text'],'Speaker:A wide continuation2');self.assertEqual(r['selectedIndices'],[0,1,2])
 def test_clipped_main_still_abstains(self):
  self.assertEqual(self.select(native(('Main',[100,420,950,490])))['reason'],'boundary_crossing_candidate')
