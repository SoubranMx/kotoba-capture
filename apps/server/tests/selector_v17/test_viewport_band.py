from .test_selector import selector,native,image,geometry,policy
import json,unittest
class ViewportBandTests(unittest.TestCase):
 def policy(self):return policy(roi=[0,.03,1,.45],mainHeight=[.045,.1],rowCenterTolerance=.025,maxRowGap=.07,minimumAnchorAspectRatio=3,auxiliaryHeightRatio=.8)
 def select(self,*boxes):return selector.select_caption_profile_v17(image(),native(*boxes),self.policy(),geometry())
 def test_fullwidth_config(self):self.assertEqual(self.policy()['roi'],[0,.03,1,.45])
 def test_viewport_long_row_retained(self):self.assertEqual(self.select(('A complete viewport-wide caption',[20,100,980,170]))['text'],'A complete viewport-wide caption')
 def test_long_three_row_dialogue_retained(self):
  self.assertEqual(self.select(('Daughter: yes',[200,80,800,150]),('Me: 2 receipts',[180,190,820,260]),('Shop: complete final response',[20,300,980,370]))['text'],'Daughter: yes\nMe: 2 receipts\nShop: complete final response')
 def test_vertical_clipping_still_abstains(self):self.assertEqual(self.select(('Caption',[20,410,980,480]))['status'],'review')
 def test_menu_second_group_still_ambiguous(self):self.assertEqual(self.select(('Caption',[20,80,980,150]),('Menu notice',[200,350,800,420]))['status'],'review')
 def test_below_height_notice_ignored(self):self.assertEqual(self.select(('Caption',[20,80,980,150]),('Small notice',[200,350,800,390]))['text'],'Caption')
