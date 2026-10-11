from .test_selector import selector,native,image,geometry,policy
import copy,hashlib,json,unittest
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def evidence(n,statuses):return dict(schema='caption-style-evidence/v1',adapterVersion='light-outline-components-v2',style='light_fill_dark_outline',imageSha256='a'*64,nativeSha256=sha(n),geometrySha256=sha(geometry()),entries=[dict(index=i,status=s,reason='synthetic') for i,s in enumerate(statuses)])
class StyleContract(unittest.TestCase):
 def select(self,n,e=None,identity='a'*64):return selector.select_caption_profile_v17(image(),n,policy(requiredVisualStyle='light_fill_dark_outline'),geometry(),style_evidence=e,expected_image_sha256=identity)
 def test_missing_fails_closed(self):self.assertEqual(self.select(native(('Main',[200,150,800,210])))['reason'],'invalid_style_evidence')
 def test_mismatch_removed_before_crossing_affiliation(self):
  n=native(('Main',[200,150,800,210]),('Handwritten panel',[200,390,800,510]));r=self.select(n,evidence(n,['match','mismatch']));self.assertEqual(r['text'],'Main');self.assertIn({'index':1,'reason':'visual_style_mismatch'},r['rejected']);self.assertEqual(r['nativeResult'],n)
 def test_unknown_crossing_still_abstains(self):
  n=native(('Main',[200,150,800,210]),('Uncertain continuation',[200,390,800,510]));self.assertEqual(self.select(n,evidence(n,['match','unknown']))['status'],'review')
 def test_unknown_selected_fails_closed(self):
  n=native(('Uncertain',[200,150,800,210]));self.assertEqual(self.select(n,evidence(n,['unknown']))['reason'],'unknown_visual_style')
 def test_two_matching_groups_still_abstain(self):
  n=native(('Main',[110,140,400,200]),('Competing',[600,320,890,380]));self.assertEqual(self.select(n,evidence(n,['match','match']))['reason'],'ambiguous_groups')
 def test_wrong_bindings_and_entries_fail_closed(self):
  n=native(('Main',[200,150,800,210]));base=evidence(n,['match'])
  for key in ['imageSha256','nativeSha256','geometrySha256','schema','style']:
   e=copy.deepcopy(base);e[key]='stale';self.assertEqual(self.select(n,e)['reason'],'invalid_style_evidence')
  for entries in [[],[dict(index=1,status='match')],[dict(index=0,status='bogus')]]:
   e=copy.deepcopy(base);e['entries']=entries;self.assertEqual(self.select(n,e)['reason'],'invalid_style_evidence')
