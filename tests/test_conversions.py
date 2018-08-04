from unittest import TestCase
from src.colormodels import RGB, HSV, LAB


class TestConversions(TestCase):
    """
    Tests to ensure that the conversions between all supported color spaces works.
    """

    test_to = 1000

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

    def test_lab_to_rgb(self):
        for i in range(TestConversions.test_to):
            lab = LAB(48, -116, 5)
            other = lab.to_rgb().to_lab()
            print(lab.output())
            print(lab.to_rgb().output())
            print(lab.to_rgb().to_lab().output())
            self.assertTrue(lab.same_color(other))

    def test_hsv_to_lab(self):
        for i in range(TestConversions.test_to):
            hsv = HSV.random_hsv()
            other = hsv.to_lab().to_hsv()
            self.assertTrue(hsv.same_color(other))

    def lab_to_hsv(self):
        pass
