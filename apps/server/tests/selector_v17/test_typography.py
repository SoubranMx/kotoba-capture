from .test_selector import selector, policy, native, image, geometry
import copy
import unittest

def guided(**updates):
    values = dict(minimumAnchorAspectRatio=3, auxiliaryHeightRatio=.8)
    values.update(updates)
    return policy(**values)
class TypographyTests(unittest.TestCase):
    def select(self,n,p=None):
        return selector.select_caption_profile_v6(image(),n,p or guided(),geometry())
    def test_admitted_upper_auxiliary_is_not_a_main_row(self):
        n=native(('auxiliary',[220,100,380,145]),('Body caption',[200,155,700,225]))
        r=self.select(n)
        self.assertEqual(r['text'],'Body caption')
        self.assertEqual(r['selectedIndices'],[1])
        self.assertEqual(r['nativeResult'],n)
    def test_multiple_main_rows_and_dialogue_labels_are_retained(self):
        n=native(('Shop: welcome!',[200,120,800,180]),('Me: 2 receipts?',[180,230,850,300]),('Shop: yes.',[240,340,780,400]))
        r=self.select(n,guided(maxRowGap=.08))
        self.assertEqual(r['text'],'Shop: welcome!\nMe: 2 receipts?\nShop: yes.')
    def test_tall_offrow_scene_sign_does_not_veto_supported_rows(self):
        r=self.select(native(('Body caption',[300,160,750,230]),('Vertical sign',[110,50,170,280])))
        self.assertEqual(r['text'],'Body caption')
    def test_small_offrow_sign_is_audited_not_joined(self):
        r=self.select(native(('Body caption',[300,160,750,230]),('Sign',[110,290,190,350])))
        self.assertEqual(r['text'],'Body caption')
    def test_square_digit_fragment_with_row_support_is_retained(self):
        r=self.select(native(('2',[180,160,250,230]),('receipts',[260,160,750,230])))
        self.assertEqual(r['text'],'2receipts')
    def test_clipped_long_continuation_still_abstains(self):
        r=self.select(native(('Body caption',[300,160,750,230]),('clipped continuation',[760,160,960,230])))
        self.assertEqual(r['status'],'review')
        self.assertEqual(r['reason'],'boundary_crossing_candidate')
    def test_competing_same_roi_sign_group_still_abstains(self):
        r=self.select(native(('Body caption',[180,120,500,180]),('Scene sign',[550,290,880,350])))
        self.assertEqual(r['status'],'review')
    def test_overlapping_main_sign_still_abstains(self):
        r=self.select(native(('Body caption',[200,160,750,230]),('Scene sign',[250,165,700,235])))
        self.assertEqual(r['status'],'review')
    def test_invalid_new_threshold_rejected(self):
        self.assertEqual(self.select(native(),guided(auxiliaryHeightRatio=1.1))['reason'],'invalid_policy')
    def test_raw_native_not_mutated(self):
        n=native(('Aux',[220,100,380,145]),('Caption',[200,155,700,225]));before=copy.deepcopy(n)
        self.select(n);self.assertEqual(n,before)
