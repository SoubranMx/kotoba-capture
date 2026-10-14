from .test_image_style import a,np,cv2,POLY,DEPENDENCIES_AVAILABLE
import unittest
@unittest.skipUnless(DEPENDENCIES_AVAILABLE, 'Optional NumPy/OpenCV unavailable')
class CalibratedStyleTests(unittest.TestCase):

    def test_real_font_like_thinner_outline(self):
        rgb = np.full((100, 640, 3), 125, np.uint8)
        cv2.putText(rgb, 'Main Caption 2', (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0, 0, 0), 7, cv2.LINE_AA)
        cv2.putText(rgb, 'Main Caption 2', (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (255, 255, 255), 5, cv2.LINE_AA)
        self.assertEqual(a.measure(rgb, [[15, 20], [470, 20], [470, 85], [15, 85]])['status'], 'match')

    def test_sparse_observation_remains_unknown(self):
        rgb = np.full((100, 640, 3), 125, np.uint8)
        cv2.rectangle(rgb, (20, 30), (25, 60), (255, 255, 255), -1)
        self.assertEqual(a.measure(rgb, POLY)['status'], 'unknown')

    def test_measured_fill_below_typed_prior_mismatch(self):
        rgb = np.full((100, 640, 3), 125, np.uint8)
        cv2.putText(rgb, 'Main Caption 2', (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0, 0, 0), 7, cv2.LINE_AA)
        cv2.putText(rgb, 'Main Caption 2', (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (255, 255, 255), 4, cv2.LINE_AA)
        self.assertEqual(a.measure(rgb, POLY)['status'], 'mismatch')
