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
            self.assertEqual(rgb.output(), rgb.to_hsv().to_rgb().output())

    def test_hsv_to_rgb(self):
        for i in range(TestConversions.test_to):
            hsv = HSV.random_hsv()
            self.assertEqual(hsv.output(), hsv.to_rgb().to_hsv().output())

    def test_rgb_to_lab(self):
        for i in range(TestConversions.test_to):
            rgb = RGB.random_rgb()
            self.assertEqual(rgb.output(), rgb.to_lab().to_rgb().output())

    def test_lab_to_rgb(self):
        for i in range(TestConversions.test_to):
            lab = LAB(48, -116, 5)
            print(lab.output())
            print(lab.to_rgb().output())
            print(lab.to_rgb().to_lab().output())
            self.assertEqual(lab.output(), lab.to_rgb().to_lab().output())

    def test_hsv_to_lab(self):
        for i in range(TestConversions.test_to):
            hsv = HSV(137, 0, 56)
            print(hsv.output())
            print(hsv.to_lab().output())
            print(hsv.to_lab().to_hsv().output(), '\n')
            #self.assertEqual(hsv.output(), hsv.to_lab().to_hsv().output())

    def lab_to_hsv(self):
        pass
