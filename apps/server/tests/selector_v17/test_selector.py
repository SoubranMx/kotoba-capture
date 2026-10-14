"""English synthetic fixtures; no image/model/reference loading."""
import copy
import math
import unittest

from kotoba_capture import selector


def policy(**changes):
    value = dict(roi=[.1,.1,.9,.4], mainHeight=[.04,.08], rowCenterTolerance=.015,
                 maxInlineGap=.05,maxRowGap=.06,minHorizontalOverlap=.2,
                 minConfidence=0,background='no_constraint',orientation='horizontal',maxRows=3)
    value.update(changes)
    return value


def geometry(width=1000,height=1000,crop=None):
    return dict(sourceWidth=width,sourceHeight=height,crop=crop or [0,0,width,height])


def image(width=1000,height=1000):
    return dict(width=width,height=height)


def native(*entries):
    values = dict(rec_texts=[],rec_scores=[],rec_boxes=[],dt_polys=[],rec_polys=[])
    for text,box in entries:
        x1,y1,x2,y2 = box
        poly = [[x1,y1],[x2,y1],[x2,y2],[x1,y2]]
        values['rec_texts'].append(text);values['rec_scores'].append(.9)
        values['rec_boxes'].append(box);values['dt_polys'].append(poly)
        values['rec_polys'].append(copy.deepcopy(poly))
    return values


class SelectorTests(unittest.TestCase):
    def run_selector(self,n=None,p=None,g=None,i=None,e=None):
        return selector.select_caption_profile_v6(i or image(),n or native(),p if p is not None else policy(),g or geometry(),blue_panel_evidence=e)

    def assert_review(self,result,reason=None):
        self.assertEqual(result['status'],'review');self.assertEqual(result['text'],'')
        self.assertTrue(result['reviewRequired'])
        if reason:self.assertEqual(result['reason'],reason)

    def test_degenerate_native_polygons_abstain(self):
        malformed = (
            [[200,150]] * 4,
            [[200,150],[300,150],[400,150],[600,150]],
        )
        for key in ('dt_polys','rec_polys'):
            for polygon in malformed:
                with self.subTest(key=key,polygon=polygon):
                    n=native(('Main',[200,150,600,200]))
                    n[key][0]=copy.deepcopy(polygon)
                    self.assert_review(self.run_selector(n),'malformed_native')

    def test_self_intersecting_native_polygons_abstain(self):
        for key in ('dt_polys','rec_polys'):
            n=native(('Main',[200,150,600,200]))
            n[key][0]=[[200,150],[600,200],[200,200],[500,150]]
            with self.subTest(key=key):
                self.assert_review(self.run_selector(n),'malformed_native')

    def test_polygon_winding_and_nonidentical_box_are_valid(self):
        for reverse in (False,True):
            n=native(('Main',[200,150,600,200]))
            polygon=[[210,152],[590,154],[580,198],[205,196]]
            n['dt_polys'][0]=copy.deepcopy(polygon[::-1] if reverse else polygon)
            n['rec_polys'][0]=copy.deepcopy(polygon[::-1] if reverse else polygon)
            with self.subTest(reverse=reverse):
                self.assertEqual(self.run_selector(n)['text'],'Main')

    def test_unrelated_exterior_sign_does_not_blank_supported_row(self):
        n=native(('Main caption',[200,150,600,200]),('Scene label',[350,395,450,455]))
        r=self.run_selector(n)
        self.assertEqual(r['text'],'Main caption')
        self.assertEqual(r['selectedIndices'],[0])
        self.assertEqual(r['nativeResult'],n)
        self.assertIn({'index':1,'reason':'boundary_crossing_unaffiliated'},r['rejected'])

    def test_same_row_crossing_signlike_fragment_remains_ambiguous(self):
        n=native(('Main',[200,150,600,200]),('Sign-like',[850,150,950,200]))
        self.assert_review(self.run_selector(n),'boundary_crossing_candidate')

    def test_clipped_wrapped_row_center_inside_roi_abstains(self):
        n=native(('First',[200,300,600,350]),('Second',[220,370,580,420]))
        self.assert_review(self.run_selector(n),'boundary_crossing_candidate')

    def test_side_clipping_continuation_abstains(self):
        n=native(('Main',[250,150,600,200]),('Clipped',[50,150,230,200]))
        self.assert_review(self.run_selector(n),'boundary_crossing_candidate')

    def test_oversized_exterior_crossing_box_still_abstains(self):
        n=native(('Main',[200,150,600,200]),('Oversized',[350,390,700,520]))
        self.assert_review(self.run_selector(n),'boundary_crossing_candidate')

    def test_small_boundary_crossing_glyph_does_not_veto(self):
        n=native(('Main',[200,330,600,380]),('Small',[230,395,280,420]))
        self.assertEqual(self.run_selector(n)['text'],'Main')

    def test_crossing_only_without_supported_row_abstains(self):
        self.assert_review(self.run_selector(native(('Clipped',[350,395,450,455]))),'boundary_crossing_candidate')

    def test_nonblue_row_needs_no_color_evidence(self):
        r=self.run_selector(native(('Main caption',[200,150,600,200])))
        self.assertEqual(r['text'],'Main caption');self.assertEqual(r['selectedIndices'],[0])
        self.assertEqual(r['profile'],'roi-guided-v17');self.assertTrue(r['reviewRequired'])

    def test_policy_is_required_no_whole_frame_fallback(self):
        self.assert_review(selector.select_caption_profile_v6(image(),native(),None,geometry()),'missing_policy')

    def test_zero_alignment_constraint_is_invalid(self):
        self.assert_review(self.run_selector(p=policy(minHorizontalOverlap=0)),'invalid_policy')

    def test_boolean_image_dimensions_invalid(self):
        self.assert_review(self.run_selector(g=geometry(1,1000),i=image(True,1000)),'invalid_geometry')

    def test_roi_missing(self):
        p=policy();del p['roi'];self.assert_review(self.run_selector(p=p),'invalid_policy')

    def test_roi_invalid_numbers_bounds_and_shape(self):
        for roi in ([0,0,1,math.nan],[0,0,math.inf,1],[-.1,0,.9,1],[.1,.1,.1,.4],[0,0,1], [False,0,1,1]):
            with self.subTest(roi=roi):self.assert_review(self.run_selector(p=policy(roi=roi)),'invalid_policy')

    def test_height_band_invalid(self):
        for value in ([0,.1],[.1,.05],[.05,1.1],[.04,math.nan]):
            self.assert_review(self.run_selector(p=policy(mainHeight=value)),'invalid_policy')

    def test_unknown_policy_reference_not_consumed(self):
        self.assert_review(self.run_selector(p=policy(reference='Do not select this')),'invalid_policy')

    def test_unsupported_orientation(self):
        self.assert_review(self.run_selector(p=policy(orientation='vertical')),'unsupported_orientation')

    def test_geometry_malformed_crop_or_size(self):
        for g in (geometry(crop=[-1,0,1000,1000]),geometry(crop=[0,0,1001,1000]),geometry(width=True),geometry(crop=[0,0,900,1000])):
            self.assert_review(self.run_selector(g=g),'invalid_geometry')

    def test_crop_roi_not_covered_is_not_negative(self):
        r=self.run_selector(g=geometry(crop=[0,0,1000,200]),i=image(1000,200))
        self.assert_review(r,'roi_not_covered');self.assertFalse(r['roiCovered'])

    def test_crop_transform_preserves_source_coordinates(self):
        n=native(('Main',[100,50,400,100]))
        p=policy(roi=[.2,.25,.7,.5])
        r=self.run_selector(n,p,geometry(crop=[100,200,700,500]),image(700,500))
        self.assertEqual(r['text'],'Main')
        self.assertEqual(r['detections'][0]['sourceGeometry'],[.2,.25,.5,.3])

    def test_resolution_invariance(self):
        a=self.run_selector(native(('Main',[200,150,600,200])))
        b=self.run_selector(native(('Main',[400,300,1200,400])),g=geometry(2000,2000),i=image(2000,2000))
        self.assertEqual(a['text'],b['text']);self.assertEqual(a['selectedIndices'],b['selectedIndices'])

    def test_lower_position_supported(self):
        r=self.run_selector(native(('Main',[200,650,600,700])),policy(roi=[.1,.6,.9,.9]))
        self.assertEqual(r['text'],'Main')

    def test_array_lengths_missing_and_nonfinite(self):
        bad=native(('Main',[200,150,600,200]));bad['rec_scores']=[]
        self.assert_review(self.run_selector(bad),'malformed_native')
        bad=native(('Main',[200,150,600,200]));bad['rec_boxes'][0][0]=math.nan
        self.assert_review(self.run_selector(bad),'malformed_native')
        bad=native(('Main',[200,150,600,200]));bad['rec_polys'][0][0][0]=math.inf
        self.assert_review(self.run_selector(bad),'malformed_native')
        bad=native(('Main',[200,150,600,200]));del bad['dt_polys']
        self.assert_review(self.run_selector(bad),'malformed_native')

    def test_native_outside_input_bounds(self):
        self.assert_review(self.run_selector(native(('Main',[200,150,1100,200]))),'malformed_native')

    def test_multiline_reading_order(self):
        r=self.run_selector(native(('Second',[200,250,600,300]),('First',[200,150,600,200])))
        self.assertEqual(r['text'],'First\nSecond');self.assertEqual(r['selectedIndices'],[1,0])

    def test_three_rows(self):
        r=self.run_selector(native(('One',[200,110,600,160]),('Two',[200,210,600,260]),('Three',[200,310,600,360])))
        self.assertEqual(r['text'],'One\nTwo\nThree')

    def test_fragment_join_and_square_digit_retained(self):
        r=self.run_selector(native(('2',[200,150,250,200]),(' platforms, left.',[260,150,600,200])))
        self.assertEqual(r['text'],'2 platforms, left.');self.assertEqual(r['selectedIndices'],[0,1])

    def test_isolated_square_needs_row_support(self):
        self.assert_review(self.run_selector(native(('2',[200,150,250,200]))),'unsupported_isolated_square')

    def test_punctuation_and_embedded_digit_not_rewritten(self):
        r=self.run_selector(native(('Route2, intact!',[200,150,600,200])))
        self.assertEqual(r['text'],'Route2, intact!')

    def test_auxiliary_candidate_excluded_not_claimed_furigana(self):
        r=self.run_selector(native(('Main',[200,180,600,230]),('aux',[230,145,280,165])))
        self.assertEqual(r['text'],'Main')
        self.assertEqual(r['rejected'][0]['reason'],'auxiliary_candidate')
        self.assertFalse(r['furiganaExtractionClaimed'])

    def test_small_unassociated_text_does_not_become_auxiliary(self):
        r=self.run_selector(native(('Main',[200,180,600,230]),('other',[700,140,760,160])))
        self.assertEqual(r['text'],'Main');self.assertEqual(r['rejected'][0]['reason'],'outside_main_height_band')

    def test_confidence_heuristic_excludes_low_score(self):
        n=native(('Main',[200,150,600,200]));n['rec_scores'][0]=.1
        self.assert_review(self.run_selector(n,policy(minConfidence=.5)),'no_supported_main_rows')

    def test_signage_outside_roi_retained_in_audit(self):
        r=self.run_selector(native(('Main',[200,150,600,200]),('Scene sign',[200,600,650,650])))
        self.assertEqual(r['text'],'Main');self.assertEqual(len(r['detections']),2)
        self.assertEqual(r['rejected'][0]['reason'],'outside_roi')

    def test_competing_sign_like_groups_inside_roi_abstain(self):
        r=self.run_selector(native(('Caption',[150,150,350,200]),('Sign',[650,150,850,200])))
        self.assert_review(r,'ambiguous_groups');self.assertEqual(len(r['candidateGroups']),2)

    def test_separated_vertical_groups_abstain(self):
        r=self.run_selector(native(('First',[200,110,600,160]),('Other',[200,330,600,380])))
        self.assert_review(r,'ambiguous_groups')

    def test_oversized_boundary_crossing_review(self):
        r=self.run_selector(native(('Spanning',[50,150,950,200]),('Main',[200,250,600,300])))
        self.assert_review(r,'boundary_crossing_candidate')

    def test_vertical_box_supported_size_abstains(self):
        self.assert_review(self.run_selector(native(('Tall',[200,150,225,200]))),'unsupported_orientation')

    def test_duplicate_overlapping_main_boxes_abstain(self):
        r=self.run_selector(native(('Main',[200,150,600,200]),('Duplicate',[205,150,605,200])))
        self.assert_review(r,'overlapping_main_boxes')

    def test_excess_rows_abstain(self):
        n=native(*[(str(i),[200,110+60*i,600,160+60*i]) for i in range(4)])
        self.assert_review(self.run_selector(n,policy(maxRows=3)),'unsupported_row_count')

    def test_blue_restriction_requires_evidence(self):
        self.assert_review(self.run_selector(native(('Main',[200,150,600,200])),policy(background='blue_panel')),'missing_blue_panel_evidence')

    def test_blue_false_evidence_abstains(self):
        e={'detected':False,'provenance':'caller_supplied'}
        self.assert_review(self.run_selector(native(('Main',[200,150,600,200])),policy(background='blue_panel'),e=e),'no_supported_blue_panel')

    def test_blue_true_evidence_is_explicit_caller_input(self):
        e={'detected':True,'bounds':[.1,.1,.9,.4],'coordinateSpace':'source_normalized','provenance':'caller_supplied'}
        r=self.run_selector(native(('Main',[200,150,600,200])),policy(background='blue_panel'),e=e)
        self.assertEqual(r['text'],'Main');self.assertFalse(r['backgroundDetectorExecuted'])
        self.assertEqual(r['backgroundEvidence'],e)

    def test_blue_evidence_wrong_coordinate_space(self):
        e={'detected':True,'bounds':[100,100,900,400],'coordinateSpace':'pixels','provenance':'caller_supplied'}
        self.assert_review(self.run_selector(native(('Main',[200,150,600,200])),policy(background='blue_panel'),e=e),'invalid_blue_panel_evidence')

    def test_complete_inputs_immutable_and_audit_independent(self):
        n=native(('Main',[200,150,600,200]));p=policy();g=geometry();before=copy.deepcopy((n,p,g))
        r=self.run_selector(n,p,g);self.assertEqual((n,p,g),before)
        r['nativeResult']['rec_texts'][0]='changed';self.assertEqual(n['rec_texts'][0],'Main')

    def test_same_geometry_different_language_text_is_not_filtered(self):
        for text in ('English','123456','Mixed-label'):
            self.assertEqual(self.run_selector(native((text,[200,150,600,200])))['text'],text)

    def test_indistinguishable_single_sign_is_only_review_candidate(self):
        r=self.run_selector(native(('Sign-like text',[200,150,600,200])))
        self.assertEqual(r['text'],'Sign-like text');self.assertTrue(r['reviewRequired'])
        self.assertFalse(r['captionIntentVerified'])

    def test_empty_native_is_review_not_guaranteed_negative(self):
        self.assert_review(self.run_selector(),'no_supported_main_rows')

if __name__=='__main__':unittest.main()
