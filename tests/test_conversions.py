from unittest import TestCase
from src.color_models import RGB, HSV, LAB


class TestConversions(TestCase):
    """
    Tests to ensure that the conversions between all supported color spaces works.
    Going from LAB color space to either RGB or HSV then back to LAB will result in
    a LAB value that not is 100% correct.
    """

    test_to = 100000

    def test_rgb_to_hsv(self):
        for i in range(TestConversions.test_to):
            rgb = RGB.random_rgb()
            other = rgb.to_hsv().to_rgb()
            self.assertTrue(rgb.same_color(other))

    def test_hsv_to_rgb(self):
        for i in range(TestConversions.test_to):
            hsv = HSV.random_hsv()
            other = hsv.to_rgb().to_hsv()
            self.assertTrue(hsv.same_color(other))

    def test_rgb_to_lab(self):
        for i in range(TestConversions.test_to):
            rgb = RGB.random_rgb()
            other = rgb.to_lab().to_rgb()
            self.assertTrue(rgb.same_color(other))

    def test_hsv_to_lab(self):
        for i in range(TestConversions.test_to):
            hsv = HSV.random_hsv()
            other = hsv.to_lab().to_hsv()
            self.assertTrue(hsv.same_color(other))
