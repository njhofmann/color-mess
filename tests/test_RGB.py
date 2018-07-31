from unittest import TestCase
from src.colormodels import RGB


class TestRGB(TestCase):

    def test_output_rgb(self):
        rgb = RGB(0, 0, 0)
        self.assertEqual(rgb.output_rgb(), (0, 0, 0))

        rgb = RGB(255, 255, 255)
        self.assertEqual(rgb.output_rgb(), (255, 255, 255))

        rgb = RGB(54, 178, 213)
        self.assertEqual(rgb.output_rgb(), (54, 178, 213))

        rgb = RGB(198, 34, 119)
        self.assertEqual(rgb.output_rgb(), (198, 34, 119))

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
        self.assertEqual(rgb.to_hsv().output_hsv_with_alpha(), (193, 74.648, 83.529, 1))

        rgb = RGB(198, 34, 119, .34)
        self.assertEqual(rgb.to_hsv().output_hsv_with_alpha(), (328, 82.828, 77.647, .34))
