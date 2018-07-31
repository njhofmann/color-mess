from unittest import TestCase
from src.colormodels import HSV


class TestHSV(TestCase):
    def test_output_to_string(self):
        hsv = HSV(360, 100, 100)
        self.assertEqual(hsv.output_to_string(), 'hsv(360, 100%, 100%)')

        hsv = HSV(0, 0, 0)
        self.assertEqual(hsv.output_to_string(), 'hsv(0, 0%, 0%)')

        hsv = HSV(250, .56, .87)
        self.assertEqual(hsv.output_to_string(), 'hsv(250, 0.56%, 0.87%)')

        hsv = HSV(132, .23, .98)
        self.assertEqual(hsv.output_to_string(), 'hsv(132, 0.23%, 0.98%)')

    def test_output_hsv_with_alpha(self):
        hsv = HSV(360, 100, 100)
        self.assertEqual(hsv.output_hsv_with_alpha(), (360, 100, 100, 1))

        hsv = HSV(0, 0, 0, .34)
        self.assertEqual(hsv.output_hsv_with_alpha(), (0, 0, 0, .34))

        hsv = HSV(250, .56, .87, .2)
        self.assertEqual(hsv.output_hsv_with_alpha(), (250, .56, .87, .2))

        hsv = HSV(132, .23, .98)
        self.assertEqual(hsv.output_hsv_with_alpha(), (132, .23, .98, 1))

    def test_to_rgb(self):
        hsv = HSV(360, 100, 100)
        #self.assertEqual(hsv.to_rgb().output_rgb(), (255, 0, 4))

        hsv = HSV(0, 0, 0)
        self.assertEqual(hsv.to_rgb().output_rgb(), (0, 0, 0))

        hsv = HSV(250, .56, .87)
        self.assertEqual(hsv.to_rgb().output_rgb(), (2, 2, 2))

        hsv = HSV(132, .23, .98)
        self.assertEqual(hsv.to_rgb().output_rgb(), (2, 2, 2))
