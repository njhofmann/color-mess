from unittest import TestCase
from src.colormodels import RGB


class TestRGBToHSVConversion(TestCase):

    def test_conversion(self):
        for i in range(1000):
            rgb = RGB.random_rgb()
            self.assertEqual(rgb.to_hsv().to_rgb().output(), rgb.output())