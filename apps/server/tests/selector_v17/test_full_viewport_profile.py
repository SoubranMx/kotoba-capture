from .test_selector import selector,native,image,geometry,policy
from .test_style_contract import evidence
import json,unittest
from pathlib import Path
class ViewportProfile(unittest.TestCase):
 def configured(self):return policy(roi=[0,0,1,1],mainHeight=[.045,.1],rowCenterTolerance=.025,maxRowGap=.07,maxRows=8,requiredVisualStyle='light_fill_dark_outline',minimumAnchorAspectRatio=5,auxiliaryHeightRatio=.8,maxHorizontalTiltDegrees=3)
 def rows(self,count):return native(*[(f'Row {i}',[150,60+i*95,850,125+i*95]) for i in range(count)])
 def select(self,n,p):return selector.select_caption_profile_v17(image(),n,p,geometry(),style_evidence=evidence(n,['match']*len(n['rec_texts'])),expected_image_sha256='a'*64)
 def test_four_five_rows_in_configured_viewport(self):
  for count in [4,5]:
   n=self.rows(count);r=self.select(n,self.configured());self.assertEqual(r['text'],'\n'.join(n['rec_texts']))
 def test_eight_rows_allowed_nine_review(self):
  p=self.configured();p['mainHeight']=[.035,.1]
  for count in [8,9]:
   n=native(*[(f'Row {i}',[100,15+i*75,900,65+i*75]) for i in range(count)])
   r=self.select(n,p);self.assertEqual(r['status'],'selected' if count==8 else 'review')
 def test_matched_separate_group_still_ambiguous(self):
  n=native(('Main',[100,100,800,170]),('Scene group',[100,600,800,670]));self.assertEqual(self.select(n,self.configured())['reason'],'ambiguous_groups')
 def test_unknown_eligible_row_still_blocks(self):
  n=native(('Main',[100,100,800,170]),('Uncertain',[100,600,800,670]));r=selector.select_caption_profile_v17(image(),n,self.configured(),geometry(),style_evidence=evidence(n,['match','unknown']),expected_image_sha256='a'*64);self.assertEqual(r['status'],'review')
 def test_auxiliary_style_mismatch_not_main_label(self):
  n=native(('Main',[100,100,800,170]),('Reading',[100,180,800,245]));r=selector.select_caption_profile_v17(image(),n,self.configured(),geometry(),style_evidence=evidence(n,['match','mismatch']),expected_image_sha256='a'*64);self.assertEqual(r['text'],'Main');self.assertEqual(r['nativeResult'],n)
