import importlib.util
import unittest

DEPENDENCIES_AVAILABLE = all(
    importlib.util.find_spec(name) is not None for name in ('numpy', 'cv2')
)
if DEPENDENCIES_AVAILABLE:
    import cv2
    import numpy as np
    from kotoba_capture import style_evidence as a
else:
    a = np = cv2 = None

POLY=[[5,5],[635,5],[635,95],[5,95]]
def raster(fill=(255,255,255),outline=True,bg=(110,130,170),thin=False):
 rgb=np.full((100,640,3),bg,dtype=np.uint8)
 if outline:cv2.putText(rgb,'Main 2: Caption',(20,75),cv2.FONT_HERSHEY_SIMPLEX,1.7,(0,0,0),10,cv2.LINE_AA)
 cv2.putText(rgb,'Main 2: Caption',(20,75),cv2.FONT_HERSHEY_SIMPLEX,1.7,fill,1 if thin else 5,cv2.LINE_AA)
 return rgb
@unittest.skipUnless(DEPENDENCIES_AVAILABLE, 'Optional NumPy/OpenCV unavailable')
class ImageStyleTests(unittest.TestCase):
 def test_outline_dark_blue_gray_bright_backgrounds(self):
  for bg in [(20,20,20),(20,60,180),(120,120,120),(245,245,245)]:
   with self.subTest(bg=bg):self.assertEqual(a.measure(raster(bg=bg),POLY)['status'],'match')
 def test_inverse_print_is_not_outline(self):self.assertNotEqual(a.measure(raster(fill=(0,0,0),outline=False,bg=(255,255,255)),POLY)['status'],'match')
 def test_thin_chalk_without_outline_unknown_not_match(self):self.assertNotEqual(a.measure(raster(outline=False,bg=(40,40,40),thin=True),POLY)['status'],'match')
 def test_colored_fill_not_match(self):self.assertNotEqual(a.measure(raster(fill=(190,80,210)),POLY)['status'],'match')
 def test_uniform_background_not_match(self):
  for v in [0,255]:self.assertEqual(a.measure(np.full((100,640,3),v,np.uint8),POLY)['status'],'mismatch')
 def test_adapter_binds_image_native_geometry(self):
  n={'rec_texts':['Main'],'rec_polys':[POLY]};g={'sourceWidth':640,'sourceHeight':100,'crop':[0,0,640,100]};r=a.from_rgb(raster(),n,g,'a'*64);self.assertEqual(r['nativeSha256'],a.binding(n));self.assertEqual(r['geometrySha256'],a.binding(g));self.assertEqual(r['imageSha256'],'a'*64)
