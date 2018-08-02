from unittest import TestCase
from src.colormodels import RGB


class TestRGB(TestCase):

    def test_output_rgb(self):
        rgb = RGB(0, 0, 0)
        self.assertEqual(rgb.output(), (0, 0, 0))

        rgb = RGB(255, 255, 255)
        self.assertEqual(rgb.output(), (255, 255, 255))

        rgb = RGB(54, 178, 213)
        self.assertEqual(rgb.output(), (54, 178, 213))

        rgb = RGB(198, 34, 119)
        self.assertEqual(rgb.output(), (198, 34, 119))

    def test_output_rgb_with_alpha(self):
        rgb = RGB(0, 0, 0, 1)
        self.assertEqual(rgb.output_rgb_with_alpha(), (0, 0, 0, 1))

        rgb = RGB(255, 255, 255, .5)
        self.assertEqual(rgb.output_rgb_with_alpha(), (255, 255, 255, .5))

        rgb = RGB(54, 178, 213, .23)
        self.assertEqual(rgb.output_rgb_with_alpha(), (54, 178, 213, .23))

        rgb = RGB(198, 34, 119, .78)
        self.assertEqual(rgb.output_rgb_with_alpha(), (198, 34, 119, .78))

    def test_to_hsv(self):
        rgb = RGB(0, 0, 0)
        self.assertEqual(rgb.to_hsv().output_hsv_with_alpha(), (0, 0, 0, 1))

        rgb = RGB(255, 255, 255, .5)
        self.assertEqual(rgb.to_hsv().output_hsv_with_alpha(), (0, 0, 100, .5))

        rgb = RGB(54, 178, 213)
        self.assertEqual(rgb.to_hsv().output_hsv_with_alpha(), (193.20754716981133, 74.64788732394366,
                                                                83.52941176470588, 1))

        rgb = RGB(198, 34, 119, .34)
        self.assertEqual(rgb.to_hsv().output_hsv_with_alpha(), (328.9024390243902, 82.82828282828282,
                                                                77.64705882352942, 0.34))
