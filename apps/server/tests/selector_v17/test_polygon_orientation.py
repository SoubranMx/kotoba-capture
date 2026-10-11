from .test_selector import selector,native,image,geometry,policy
from .test_style_contract import evidence
import math,copy,unittest

def quad(degrees,width=220,height=45,center=(220,325)):
 a=math.radians(degrees);c,s=math.cos(a),math.sin(a)
 return [[center[0]+x*c-y*s,center[1]+x*s+y*c] for x,y in [(-width/2,-height/2),(width/2,-height/2),(width/2,height/2),(-width/2,height/2)]]
def fixture(dt=11,rec=11):
 n=native(('Main caption',[300,120,750,190]),('Printed group',[110,290,330,360]));n['dt_polys'][1]=quad(dt);n['rec_polys'][1]=quad(rec);return n
class PolygonOrientation(unittest.TestCase):
 def select(self,n,limit=5):
  p=policy(requiredVisualStyle='light_fill_dark_outline',minimumAnchorAspectRatio=3,auxiliaryHeightRatio=.8)
  if limit is not None:p['maxHorizontalTiltDegrees']=limit
  return selector.select_caption_profile_v17(image(),n,p,geometry(),style_evidence=evidence(n,['match','unknown']),expected_image_sha256='a'*64)
 def test_rotated_unknown_group_excluded_by_explicit_prior(self):
  n=fixture();before=copy.deepcopy(n);r=self.select(n);self.assertEqual(r['text'],'Main caption');self.assertIn(dict(index=1,reason='outside_horizontal_orientation_prior'),r['rejected']);self.assertEqual(r['styleEvidence']['entries'][1]['status'],'unknown');self.assertEqual(n,before)
 def test_absent_policy_preserves_ambiguity(self):self.assertEqual(self.select(fixture(),None)['reason'],'ambiguous_groups')
 def test_cyclic_reverse_and_negative_angle(self):
  for angle in [11,-11,89,-89]:
   for rotation in range(4):
    for reverse in [False,True]:
     n=fixture(angle,angle)
     for key in ['dt_polys','rec_polys']:
      p=n[key][1];p=p[rotation:]+p[:rotation];n[key][1]=p[::-1] if reverse else p
     self.assertEqual(self.select(n)['text'],'Main caption')
 def test_at_threshold_not_excluded(self):self.assertEqual(self.select(fixture(5,5))['status'],'review')
 def test_angle_jitter_consistent(self):self.assertEqual(self.select(fixture(10,11))['text'],'Main caption')
 def test_conflicting_dt_rec_is_indeterminate(self):self.assertEqual(self.select(fixture(11,0))['status'],'review')
 def test_opposite_edge_conflict_indeterminate(self):
  n=fixture();n['dt_polys'][1]=[[110,290],[330,335],[330,360],[110,360]];self.assertEqual(self.select(n)['status'],'review')
 def test_near_horizontal_unknown_still_review(self):self.assertEqual(self.select(fixture(1,1))['status'],'review')
 def test_near_square_indeterminate(self):
  n=fixture();n['dt_polys'][1]=quad(11,80,75);n['rec_polys'][1]=quad(11,80,75);self.assertEqual(self.select(n)['status'],'review')
 def test_no_anchor_tilted_main_remains_review(self):
  n=native(('Tilted candidate',[300,120,750,190]));n['dt_polys'][0]=quad(11,400,60,(500,160));n['rec_polys'][0]=copy.deepcopy(n['dt_polys'][0]);p=policy(maxHorizontalTiltDegrees=5);r=selector.select_caption_profile_v17(image(),n,p,geometry());self.assertEqual(r['status'],'review');self.assertEqual(r['reason'],'no_supported_main_rows')
 def test_zero_valid_and_invalid_limits(self):
  self.assertEqual(self.select(fixture(),0)['text'],'Main caption')
  for value in [-1,45,90,float('nan'),float('inf'),True,'5']:
   self.assertEqual(self.select(fixture(),value)['reason'],'invalid_policy')
 def test_inline_digits_and_clipping_still_conservative(self):
  n=native(('2',[180,150,240,210]),('receipts',[250,150,800,210]));p=policy(maxHorizontalTiltDegrees=5);r=selector.select_caption_profile_v17(image(),n,p,geometry());self.assertEqual(r['text'],'2receipts')
  n=native(('Main',[200,150,800,210]),('Clipped',[800,150,980,210]));self.assertEqual(selector.select_caption_profile_v17(image(),n,p,geometry())['reason'],'boundary_crossing_candidate')
