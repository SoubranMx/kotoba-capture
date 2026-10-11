"""Dependency-free opt-in ROI/typography selector, not an intent detector.

Coordinates in policy/evidence are normalized original-source bounds. Native
boxes are crop-local pixels. No models, references, color detector or v5 import
are executed; blue constraints require explicit caller-supplied evidence.
"""
from copy import deepcopy
import hashlib
import json
import math

PROFILE = 'roi-guided-v17'
_POLICY_KEYS = {'roi','mainHeight','rowCenterTolerance','maxInlineGap','maxRowGap',
                'minHorizontalOverlap','minConfidence','background','orientation','maxRows',
                'minimumAnchorAspectRatio','auxiliaryHeightRatio','requiredVisualStyle','styleRequired','maxHorizontalTiltDegrees'}
_REQUIRED_KEYS = {'roi','mainHeight','rowCenterTolerance','maxInlineGap','maxRowGap','minHorizontalOverlap'}
_NATIVE_KEYS = ('rec_texts','rec_scores','rec_boxes','dt_polys','rec_polys')


def _number(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)


def _bounds(value):
    return (isinstance(value,(list,tuple)) and len(value)==4 and all(_number(v) for v in value)
            and 0<=value[0]<value[2]<=1 and 0<=value[1]<value[3]<=1)


def _valid_policy(policy):
    if not isinstance(policy,dict) or set(policy)-_POLICY_KEYS or not _REQUIRED_KEYS.issubset(policy):
        return False
    if 'styleRequired' in policy and type(policy['styleRequired']) is not bool:
        return False
    if policy.get('styleRequired') is True and policy.get('requiredVisualStyle')!='light_fill_dark_outline':
        return False
    if 'requiredVisualStyle' in policy and policy['requiredVisualStyle']!='light_fill_dark_outline':
        return False
    if 'maxHorizontalTiltDegrees' in policy:
        limit = policy['maxHorizontalTiltDegrees']
        if not _number(limit) or not 0<=limit<45:
            return False
    band = policy['mainHeight']
    if not _bounds(policy['roi']) or not isinstance(band,(list,tuple)) or len(band)!=2:
        return False
    if not all(_number(v) for v in band) or not 0<band[0]<=band[1]<=1:
        return False
    for key in ('rowCenterTolerance','maxInlineGap','maxRowGap','minHorizontalOverlap'):
        if not _number(policy[key]) or not 0<=policy[key]<=1:
            return False
    if policy['minHorizontalOverlap']<=0:
        return False
    aspect = policy.get('minimumAnchorAspectRatio', 0)
    auxiliary = policy.get('auxiliaryHeightRatio', 0)
    if not _number(aspect) or not 0<=aspect<=100 or not _number(auxiliary) or not 0<=auxiliary<1:
        return False
    confidence = policy.get('minConfidence',0)
    rows = policy.get('maxRows',3)
    return (_number(confidence) and 0<=confidence<=1 and isinstance(rows,int)
            and not isinstance(rows,bool) and rows>=1
            and policy.get('background','no_constraint') in ('no_constraint','blue_panel'))


def _valid_geometry(image,geometry):
    if not isinstance(geometry,dict) or set(geometry)!={'sourceWidth','sourceHeight','crop'}:
        return False
    sw,sh = geometry['sourceWidth'],geometry['sourceHeight']
    if not all(isinstance(v,int) and not isinstance(v,bool) and v>0 for v in (sw,sh)):
        return False
    crop = geometry['crop']
    if not isinstance(crop,(list,tuple)) or len(crop)!=4:
        return False
    if not all(isinstance(v,int) and not isinstance(v,bool) for v in crop):
        return False
    x,y,w,h = crop
    if min(x,y)<0 or min(w,h)<=0 or x+w>sw or y+h>sh:
        return False
    if isinstance(image,dict):
        iw,ih = image.get('width'),image.get('height')
    else:
        shape = getattr(image,'shape',None)
        if shape is None or len(shape)!=3 or shape[2]!=3:
            return False
        ih,iw = shape[:2]
    return (isinstance(iw,int) and not isinstance(iw,bool) and isinstance(ih,int)
            and not isinstance(ih,bool) and iw==w and ih==h)


def _contains(outer,inner):
    epsilon = 1e-10
    return (outer[0]-epsilon<=inner[0] and outer[1]-epsilon<=inner[1]
            and outer[2]+epsilon>=inner[2] and outer[3]+epsilon>=inner[3])


def _intersection(a,b):
    return max(0,min(a[2],b[2])-max(a[0],b[0])) * max(0,min(a[3],b[3])-max(a[1],b[1]))


def _horizontal_overlap(a,b):
    intersection = max(0,min(a[2],b[2])-max(a[0],b[0]))
    return intersection/max(1e-12,min(a[2]-a[0],b[2]-b[0]))


def _raw_audit(native):
    if not isinstance(native,dict) or not isinstance(native.get('rec_texts'),list):
        return []
    audit = []
    for index,text in enumerate(native['rec_texts']):
        row = {'index':index,'text':deepcopy(text)}
        for key in _NATIVE_KEYS[1:]:
            values = native.get(key)
            row[key] = deepcopy(values[index]) if isinstance(values,list) and index<len(values) else None
        audit.append(row)
    return audit


def _simple_positive_area(polygon):
    """Admit simple nondegenerate quadrilaterals in either winding order.

    Coordinate shape/finite bounds are checked by the caller. Scale first to
    avoid overflow in orientation products; no box/polygon equality is assumed.
    """
    if len({tuple(point) for point in polygon}) != 4:
        return False
    scale = max(abs(value) for point in polygon for value in point)
    if scale == 0:
        return False
    points = [(point[0]/scale,point[1]/scale) for point in polygon]

    def cross(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

    def on_segment(a,b,c):
        return min(a[0],b[0])<=c[0]<=max(a[0],b[0]) and min(a[1],b[1])<=c[1]<=max(a[1],b[1])

    def intersect(a,b,c,d):
        ab_c,ab_d,cd_a,cd_b = cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
        if ((ab_c<0<ab_d or ab_d<0<ab_c)
                and (cd_a<0<cd_b or cd_b<0<cd_a)):
            return True
        return ((ab_c==0 and on_segment(a,b,c)) or (ab_d==0 and on_segment(a,b,d))
                or (cd_a==0 and on_segment(c,d,a)) or (cd_b==0 and on_segment(c,d,b)))

    a,b,c,d = points
    if intersect(a,b,c,d) or intersect(b,c,d,a):
        return False
    # Triangulate relative to the first vertex, avoiding shoelace cancellation.
    return abs(cross(a,b,c)+cross(a,c,d)) > 0


def _detections(native,geometry):
    if not isinstance(native,dict) or any(not isinstance(native.get(k),list) for k in _NATIVE_KEYS):
        return None
    n = len(native['rec_texts'])
    if any(len(native[k])!=n for k in _NATIVE_KEYS):
        return None
    x,y,w,h = geometry['crop']
    sw,sh = geometry['sourceWidth'],geometry['sourceHeight']
    result = []
    for index in range(n):
        text,score,box = native['rec_texts'][index],native['rec_scores'][index],native['rec_boxes'][index]
        if not isinstance(text,str) or not _number(score) or not 0<=score<=1:
            return None
        if not isinstance(box,(list,tuple)) or len(box)!=4 or not all(_number(v) for v in box):
            return None
        x1,y1,x2,y2 = box
        if not 0<=x1<x2<=w or not 0<=y1<y2<=h:
            return None
        for key in ('dt_polys','rec_polys'):
            polygon = native[key][index]
            if not isinstance(polygon,(list,tuple)) or len(polygon)!=4:
                return None
            for point in polygon:
                if (not isinstance(point,(list,tuple)) or len(point)!=2 or not all(_number(v) for v in point)
                        or not 0<=point[0]<=w or not 0<=point[1]<=h):
                    return None
            if not _simple_positive_area(polygon):
                return None
        source = [(x+x1)/sw,(y+y1)/sh,(x+x2)/sw,(y+y2)/sh]
        result.append({'index':index,'text':text,'confidence':score,'box':deepcopy(box),
                       'dtPoly':deepcopy(native['dt_polys'][index]),'recPoly':deepcopy(native['rec_polys'][index]),
                       'sourceGeometry':source,'height':(y2-y1)/sh,'centerY':(source[1]+source[3])/2,
                       'pixelWidth':x2-x1,'pixelHeight':y2-y1})
    return result


def _review(result,reason):
    result['reason'] = reason
    present = {row['index'] for row in result['rejected']}
    result['rejected'].extend({'index':d['index'],'reason':reason}
                              for d in result['detections'] if d['index'] not in present)
    return result


def _chunks(main,policy):
    # A bounded center span avoids transitive chaining between distinct rows.
    bands = []
    for detection in sorted(main,key=lambda d:(d['centerY'],d['sourceGeometry'][0],d['index'])):
        if bands and detection['centerY']-bands[-1][0]['centerY']<=policy['rowCenterTolerance']:
            bands[-1].append(detection)
        else:
            bands.append([detection])
    chunks = []
    for row_id,band in enumerate(bands):
        ordered = sorted(band,key=lambda d:(d['sourceGeometry'][0],d['index']))
        current = []
        for detection in ordered:
            if current and detection['sourceGeometry'][0]-current[-1]['sourceGeometry'][2]>policy['maxInlineGap']:
                chunks.append((row_id,current))
                current = []
            current.append(detection)
        chunks.append((row_id,current))
    rows = []
    for row_id,items in chunks:
        bounds = [min(d['sourceGeometry'][0] for d in items),min(d['sourceGeometry'][1] for d in items),
                  max(d['sourceGeometry'][2] for d in items),max(d['sourceGeometry'][3] for d in items)]
        rows.append({'rowId':row_id,'items':items,'bounds':bounds,
                     'indices':[d['index'] for d in items],'text':''.join(d['text'] for d in items)})
    return rows


def _groups(rows,policy):
    edges = [set() for _ in rows]
    for i,a in enumerate(rows):
        for j in range(i+1,len(rows)):
            b = rows[j]
            if a['rowId']==b['rowId']:
                continue
            upper,lower = sorted((a,b),key=lambda r:r['bounds'][1])
            gap = max(0,lower['bounds'][1]-upper['bounds'][3])
            if gap<=policy['maxRowGap'] and _horizontal_overlap(a['bounds'],b['bounds'])>=policy['minHorizontalOverlap']:
                edges[i].add(j);edges[j].add(i)
    groups,seen = [],set()
    for start in range(len(rows)):
        if start in seen:
            continue
        stack,indices = [start],[]
        while stack:
            index = stack.pop()
            if index in seen:
                continue
            seen.add(index);indices.append(index);stack.extend(edges[index]-seen)
        groups.append(sorted((rows[i] for i in indices),key=lambda r:(r['bounds'][1],r['bounds'][0])))
    return groups


def _boundary_affiliated(detection,main,policy):
    """Crossing evidence vetoes only plausible in-ROI caption continuations.

    An explicit ROI is the authority: a normal-sized box centered outside it
    and vertically separated from supported rows stays audited, not selected.
    Oversized evidence and absence of any anchor remain conservative.
    """
    if not main:
        return True
    if detection['height']>policy['mainHeight'][1]:
        # Out-of-profile evidence remains a veto unless every admitted anchor
        # is horizontally disjoint and beyond the configured inline distance.
        box = detection['sourceGeometry']
        separated = all(
            min(box[2],a['sourceGeometry'][2])<=max(box[0],a['sourceGeometry'][0])
            and max(0,box[0]-a['sourceGeometry'][2],a['sourceGeometry'][0]-box[2])>policy['maxInlineGap']+1e-12
            for a in main)
        return not separated
    box = detection['sourceGeometry']
    roi = policy['roi']
    center_x = (box[0]+box[2])/2
    if roi[0]<=center_x<=roi[2] and roi[1]<=detection['centerY']<=roi[3]:
        return True
    for anchor in main:
        row_box = anchor['sourceGeometry']
        if min(box[3],row_box[3])>max(box[1],row_box[1]):
            return True
        inline_gap = max(0,box[0]-row_box[2],row_box[0]-box[2])
        if (abs(detection['centerY']-anchor['centerY'])<=policy['rowCenterTolerance']
                and inline_gap<=policy['maxInlineGap']):
            return True
    return False


def _typographic_exclusions(detections, policy, trusted_anchors=None):
    """Optional explicit source typography, not an automatic sign classifier.

    Only fully covered wide rows of admitted height anchor this rule. Short
    fragments survive when aligned with an anchor. Smaller upper observations
    are auxiliary candidates, never rewritten or claimed proven furigana.
    With no anchor, preserve conservative legacy admission/abstention.
    """
    aspect = policy.get('minimumAnchorAspectRatio', 0)
    ratio = policy.get('auxiliaryHeightRatio', 0)
    if not aspect and not ratio:
        return {}
    minimum, maximum = policy['mainHeight']
    anchor_pool = detections if trusted_anchors is None else trusted_anchors
    anchors = [d for d in anchor_pool if d['text'].strip()
               and minimum<=d['height']<=maximum
               and d['confidence']>=policy.get('minConfidence',0)
               and _contains(policy['roi'],d['sourceGeometry'])
               and d['pixelWidth']/d['pixelHeight']>=max(1,aspect)]
    exclusions = {}
    for detection in detections:
        if not _intersection(detection['sourceGeometry'],policy['roi']):
            continue
        box = detection['sourceGeometry']
        auxiliary = any(detection['index']!=a['index']
            and detection['height']<=ratio*a['height']
            and box[3]<=a['centerY']
            and max(0,a['sourceGeometry'][1]-box[3])<=policy['maxRowGap']
            and _horizontal_overlap(box,a['sourceGeometry'])>0 for a in anchors)
        if auxiliary:
            exclusions[detection['index']] = 'relative_upper_auxiliary_candidate'
            continue
        if aspect and anchors and detection['pixelWidth']/detection['pixelHeight']<aspect:
            supported = any(minimum<=detection['height']<=maximum
                and abs(detection['centerY']-a['centerY'])<=policy['rowCenterTolerance']
                and max(0,box[0]-a['sourceGeometry'][2],a['sourceGeometry'][0]-box[2])<=policy['maxInlineGap']
                for a in anchors)
            if not supported:
                exclusions[detection['index']] = 'unaffiliated_nonrow_typography'
    return exclusions



def _polygon_long_axis_angles(polygon):
    """Reliable elongation only: convex quad, long edges >=1.5*short edges.

    Cyclic vertex starts and either winding are equivalent. Concave/near-square
    shapes do not establish a text baseline and remain indeterminate.
    """
    edges = [(polygon[(i+1)%4][0]-polygon[i][0],
              polygon[(i+1)%4][1]-polygon[i][1]) for i in range(4)]
    turns = [edges[i][0]*edges[(i+1)%4][1]-edges[i][1]*edges[(i+1)%4][0] for i in range(4)]
    if not (all(v>0 for v in turns) or all(v<0 for v in turns)):
        return None
    lengths = [math.hypot(x,y) for x,y in edges]
    pair = (0,2) if lengths[0]+lengths[2]>lengths[1]+lengths[3] else (1,3)
    other = (1,3) if pair==(0,2) else (0,2)
    if min(lengths[i] for i in pair)<1.5*max(lengths[i] for i in other):
        return None
    return [(math.degrees(math.atan2(edges[i][1],edges[i][0]))+90)%180-90 for i in pair]


def _orientation_evidence(detections,limit):
    """Both opposite edges in DT and REC must support one tilted line axis.

    Nominal layout tolerances, not learned confidence: 2deg maximum pairwise
    line-axis disagreement, 1e-9deg equality tolerance. Missing/contradictory
    elongation cannot justify exclusion. Axis directions are modulo180deg.
    """
    evidence = []
    for detection in detections:
        pairs = [_polygon_long_axis_angles(detection[key]) for key in ('dtPoly','recPoly')]
        entry = {'index':detection['index'],'status':'indeterminate','reason':'unreliable_polygon_axis'}
        if all(pair is not None for pair in pairs):
            angles = pairs[0]+pairs[1]
            entry['anglesDegrees'] = angles
            consistent = all(abs((a-b+90)%180-90)<=2+1e-9 for a in angles for b in angles)
            if consistent:
                outside = all(abs(a)>limit+1e-9 for a in angles)
                entry.update(status='outside_prior' if outside else 'within_or_near_prior',reason='consistent_polygon_long_axis')
            else:
                entry['reason'] = 'inconsistent_polygon_axes'
        evidence.append(entry)
    return evidence


def _style_binding(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def _valid_style_evidence(evidence,identity,native,geometry,style):
    try:
        if not isinstance(identity,str) or len(identity)!=64 or any(c not in '0123456789abcdef' for c in identity):return False
        if not isinstance(evidence,dict) or evidence.get('schema')!='caption-style-evidence/v1' or evidence.get('style')!=style:return False
        if evidence.get('adapterVersion')!='light-outline-components-v2':return False
        if evidence.get('imageSha256')!=identity or evidence.get('nativeSha256')!=_style_binding(native) or evidence.get('geometrySha256')!=_style_binding(geometry):return False
        entries=evidence.get('entries')
        if not isinstance(entries,list) or len(entries)!=len(native['rec_texts']):return False
        return all(isinstance(e,dict) and type(e.get('index')) is int and e['index']==i and e.get('status') in ('match','mismatch','unknown') and isinstance(e.get('reason'),str) and bool(e['reason']) for i,e in enumerate(entries))
    except (ValueError,TypeError,KeyError):return False

def select_caption_profile_v6(image,native_result,policy,frame_geometry,*,blue_panel_evidence=None,style_evidence=None,expected_image_sha256=None):
    """Select an explicitly constrained candidate; every result needs review.

    `image` may be a shape-bearing BGR array or dimension metadata for cached
    geometry-only replay. Background evidence is caller input, not proof that
    this function ran or verified a detector. References are not accepted.
    """
    result = {'profile':PROFILE,'status':'review','reason':None,'text':'','selectedIndices':[],
              'rows':[],'candidateGroups':[],'rejected':[],'roiCovered':False,'reviewRequired':True,
              'captionIntentVerified':False,'furiganaExtractionClaimed':False,'backgroundDetectorExecuted':False,
              'confidenceIsCalibrated':False,
              'policy':deepcopy(policy),'frameGeometry':deepcopy(frame_geometry),
              'backgroundEvidence':deepcopy(blue_panel_evidence),'nativeResult':deepcopy(native_result),
              'detections':_raw_audit(native_result)}
    if policy is None:
        return _review(result,'missing_policy')
    if not _valid_policy(policy):
        return _review(result,'invalid_policy')
    if policy.get('orientation','horizontal')!='horizontal':
        return _review(result,'unsupported_orientation')
    if not _valid_geometry(image,frame_geometry):
        return _review(result,'invalid_geometry')
    x,y,w,h = frame_geometry['crop']
    sw,sh = frame_geometry['sourceWidth'],frame_geometry['sourceHeight']
    coverage = [x/sw,y/sh,(x+w)/sw,(y+h)/sh]
    if not _contains(coverage,policy['roi']):
        return _review(result,'roi_not_covered')
    result['roiCovered'] = True
    detections = _detections(native_result,frame_geometry)
    if detections is None:
        return _review(result,'malformed_native')
    result['detections'] = deepcopy(detections)
    panel = None
    if policy.get('background','no_constraint')=='blue_panel':
        evidence = blue_panel_evidence
        if evidence is None:
            return _review(result,'missing_blue_panel_evidence')
        if not isinstance(evidence,dict) or not isinstance(evidence.get('detected'),bool):
            return _review(result,'invalid_blue_panel_evidence')
        if evidence['detected'] is False:
            return _review(result,'no_supported_blue_panel')
        if (not _bounds(evidence.get('bounds')) or evidence.get('coordinateSpace')!='source_normalized'
                or not isinstance(evidence.get('provenance'),str) or not evidence['provenance'].strip()):
            return _review(result,'invalid_blue_panel_evidence')
        panel = evidence['bounds']
    required_style = policy.get('requiredVisualStyle') if policy.get('styleRequired', 'requiredVisualStyle' in policy) else None
    statuses = {}
    if required_style is not None:
        if required_style!='light_fill_dark_outline' or not _valid_style_evidence(style_evidence,expected_image_sha256,native_result,frame_geometry,required_style):
            return _review(result,'invalid_style_evidence')
        result['styleEvidence'] = deepcopy(style_evidence)
        statuses = {e['index']:e['status'] for e in style_evidence['entries']}
        active = [d for d in detections if statuses[d['index']]!='mismatch']
    else:
        active = detections
    orientation_exclusions = set()
    if 'maxHorizontalTiltDegrees' in policy:
        result['orientationEvidence'] = _orientation_evidence(detections,policy['maxHorizontalTiltDegrees'])
        orientation_exclusions = {e['index'] for e in result['orientationEvidence'] if e['status']=='outside_prior'}
        active = [d for d in active if d['index'] not in orientation_exclusions]
    # Geometry exclusions remain independent of uncertain physical style.
    # Only measured style matches may anchor exclusions in required-style mode.
    trusted = [d for d in active if statuses[d['index']]=='match'] if required_style else None
    typographic_exclusions = _typographic_exclusions(active,policy,trusted)
    main,small = [],[]
    crossing,vertical = [],False
    minimum,maximum = policy['mainHeight']
    for detection in detections:
        box = detection['sourceGeometry']
        reason = None
        if statuses.get(detection['index'])=='mismatch':
            reason = 'visual_style_mismatch'
        elif detection['index'] in orientation_exclusions:
            reason = 'outside_horizontal_orientation_prior'
        elif detection['index'] in typographic_exclusions:
            reason = typographic_exclusions[detection['index']]
        elif not _intersection(box,policy['roi']):
            reason = 'outside_roi'
        elif not _contains(policy['roi'],box):
            reason = 'boundary_crossing_candidate'
            if detection['text'].strip() and detection['height']>=minimum:
                crossing.append(detection)
        elif not detection['text'].strip():
            reason = 'empty_text'
        elif detection['confidence']<policy.get('minConfidence',0):
            reason = 'low_confidence_heuristic'
        elif panel is not None and not _contains(panel,box):
            reason = 'outside_supported_blue_panel'
        elif detection['height']<minimum:
            small.append(detection)
            continue
        elif detection['height']>maximum:
            reason = 'outside_main_height_band'
        elif detection['pixelWidth']<detection['pixelHeight']:
            reason = 'unsupported_orientation';vertical = True
        else:
            main.append(detection)
            continue
        result['rejected'].append({'index':detection['index'],'reason':reason})
    for detection in small:
        box = detection['sourceGeometry']
        associated = any(box[3]<=d['centerY'] and max(0,d['sourceGeometry'][1]-box[3])<=policy['maxRowGap']
                         and _horizontal_overlap(box,d['sourceGeometry'])>0 for d in main)
        result['rejected'].append({'index':detection['index'],
                                   'reason':'auxiliary_candidate' if associated else 'outside_main_height_band'})
    affiliated = [d for d in crossing if _boundary_affiliated(d,main,policy)]
    unaffiliated = {d['index'] for d in crossing if d not in affiliated}
    for rejection in result['rejected']:
        if rejection['index'] in unaffiliated:
            rejection['reason'] = 'boundary_crossing_unaffiliated'
    if affiliated:
        return _review(result,'boundary_crossing_candidate')
    if vertical:
        return _review(result,'unsupported_orientation')
    if not main:
        return _review(result,'no_supported_main_rows')
    for i,a in enumerate(main):
        for b in main[i+1:]:
            area = min((a['sourceGeometry'][2]-a['sourceGeometry'][0])*a['height'],
                       (b['sourceGeometry'][2]-b['sourceGeometry'][0])*b['height'])
            if _intersection(a['sourceGeometry'],b['sourceGeometry'])>area*.5:
                return _review(result,'overlapping_main_boxes')
    rows = _chunks(main,policy)
    groups = _groups(rows,policy)
    result['candidateGroups'] = [[{'indices':r['indices'],'bounds':r['bounds'],'text':r['text']} for r in group]
                                  for group in groups]
    if len(groups)!=1 or any(len({r['rowId'] for r in group})!=len(group) for group in groups):
        return _review(result,'ambiguous_groups')
    chosen = groups[0]
    if required_style and any(statuses[item['index']]!='match' for row in chosen for item in row['items']):
        return _review(result,'unknown_visual_style')
    if len(chosen)>policy.get('maxRows',3):
        return _review(result,'unsupported_row_count')
    if any(len(row['items'])==1 and row['items'][0]['pixelWidth']<=row['items'][0]['pixelHeight'] for row in chosen):
        return _review(result,'unsupported_isolated_square')
    result.update(status='selected',reason='unique_roi_typography_group',
                  text='\n'.join(row['text'] for row in chosen),
                  selectedIndices=[index for row in chosen for index in row['indices']],
                  rows=[{'indices':row['indices'],'bounds':row['bounds'],'text':row['text']} for row in chosen])
    return result

# Explicit versioned entry point; compatibility alias supports inherited tests.
select_caption_profile_v17 = select_caption_profile_v6
