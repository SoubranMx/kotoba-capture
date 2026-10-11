"""Private local image adapter; measurements are style heuristics, not intent."""
import hashlib,json,math
from pathlib import Path
import cv2
import numpy as np
VERSION='light-outline-components-v2'
def binding(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def measure(rgb,poly):
 points=np.asarray(poly,dtype=float)
 if points.shape!=(4,2) or not np.isfinite(points).all():return {'status':'unknown','reason':'invalid_polygon'}
 h,w=rgb.shape[:2];x0=max(0,int(math.floor(points[:,0].min())));y0=max(0,int(math.floor(points[:,1].min())));x1=min(w,int(math.ceil(points[:,0].max())));y1=min(h,int(math.ceil(points[:,1].max())))
 if x1<=x0 or y1<=y0:return {'status':'unknown','reason':'empty_crop'}
 crop=rgb[y0:y1,x0:x1];bh,bw=crop.shape[:2];low=crop.min(2);high=crop.max(2);white=((low>=200)&((high.astype(int)-low.astype(int))<=40)).astype('uint8');dark=(high<=70);area=white.size
 count,labels,stats,_=cv2.connectedComponentsWithStats(white,8);accepted=np.zeros_like(white);components=[]
 for i in range(1,count):
  x,y,cw,ch,size=map(int,stats[i]);touch=x==0 or y==0 or x+cw==bw or y+ch==bh
  if size<max(3,.00015*area) or ch<max(3,.10*bh):continue
  if size>.30*area or (touch and cw>.55*bw and ch>.70*bh):continue
  accepted[labels==i]=1;components.append((x,y,cw,ch,size))
 fill=float(accepted.mean());white_fraction=float(white.mean())
 if not components:
  return dict(status='mismatch' if white_fraction<.025 or white_fraction>.70 else 'unknown',reason='no_supported_light_glyph_components',whiteFraction=white_fraction,fillFraction=fill,components=0)
 scale=max(1,int(round(bh*.025)));outer=cv2.dilate(accepted,np.ones((2*scale+1,2*scale+1),'uint8'));ring=(outer>0)&(accepted==0);rim=float(dark[ring].mean()) if ring.any() else 0
 dist=cv2.distanceTransform(accepted,cv2.DIST_L2,5);thickness=float(np.percentile(dist[accepted>0],75)/bh)
 spread=(max(x+cw for x,y,cw,ch,size in components)-min(x for x,y,cw,ch,size in components))/bw
 # Repeated light glyphs, substantial fill/strokes and local dark outline.
 # Unknown is retained for plausible but unproven light text; never coerced away.
 adequate = bh>=8 and int(accepted.sum())>=16 and fill>=.035 and spread>=.50 and (len(components)>=3 or fill>=.15)
 if adequate and fill>=.10 and rim>=.20 and thickness>=.02:status='match';reason='supported_light_fill_dark_rim'
 elif white_fraction>.70 or (adequate and (fill<.10 or rim<.20 or thickness<.02)):status='mismatch';reason='measured_incompatible_light_fill_outline'
 else:status='unknown';reason='insufficient_style_support'
 return dict(status=status,reason=reason,whiteFraction=white_fraction,fillFraction=fill,components=len(components),darkRimFraction=rim,strokeThicknessRatio=thickness,horizontalSupport=spread,adequatelySampled=bool(adequate))
def from_rgb(rgb,native,geometry,image_sha):
 if not isinstance(rgb,np.ndarray) or rgb.dtype!=np.uint8 or rgb.ndim!=3 or rgb.shape[2]!=3:raise ValueError('RGB uint8 image required')
 if list(rgb.shape[:2])!=[geometry['crop'][3],geometry['crop'][2]]:raise ValueError('Crop geometry mismatch')
 entries=[dict(index=i,**measure(rgb,p)) for i,p in enumerate(native['rec_polys'])]
 return dict(schema='caption-style-evidence/v1',adapterVersion=VERSION,style='light_fill_dark_outline',imageSha256=image_sha,nativeSha256=binding(native),geometrySha256=binding(geometry),entries=entries)
def from_path(path,native,geometry):
 p=Path(path);raw=p.read_bytes();bgr=cv2.imdecode(np.frombuffer(raw,dtype=np.uint8),cv2.IMREAD_COLOR)
 if bgr is None:raise ValueError('Image decode failed')
 return from_rgb(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB),native,geometry,hashlib.sha256(raw).hexdigest())
