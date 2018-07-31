import colorsys
import random
import math


class RGB:
    min_value = 0
    max_value = 255
    alpha_max = 1

    def __init__(self, red, green, blue, alpha=1):
        if (not (RGB.min_value <= red <= RGB.max_value)) \
                or (not (RGB.min_value <= green <= RGB.max_value)) \
                or (not (RGB.min_value <= blue <= RGB.max_value)):
            raise ValueError('RGB values must be ints in range [0, 255]!')

        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def output_rgb(self):
        to_return = (self.red, self.green, self.blue)
        return to_return

    def output_rgb_with_alpha(self):
        to_return = (self.red, self.green, self.blue, self.alpha)
        return to_return

    def to_hsv(self):
        red = self.red / 255
        green = self.green / 255
        blue = self.blue / 255

        c_max = max(red, green, blue)
        c_min = min(red, green, blue)
        delta = c_max - c_min

        if delta == 0:
            hue = 0
        elif c_max == red:
            hue = 60 * (((green - blue) / delta) % 6)
        elif c_max == green:
            hue = 60 * (((blue - red) / delta) + 2)
        elif c_max == blue:
            hue = 60 * (((red - green) / delta) + 4)

        if c_max == 0:
            saturation = 0
        else:
            saturation = (delta / c_max) * 100

        value = c_max * 100

        return HSV(hue, saturation, value, self.alpha)

    @staticmethod
    def random_rgb():
        red = random.randint(RGB.min_value, RGB.max_value)
        green = random.randint(RGB.min_value, RGB.max_value)
        blue = random.randint(RGB.min_value, RGB.max_value)
        return RGB(red, green, blue)

    @staticmethod
    def random_rgb_with_alpha():
        red = random.randint(RGB.min_value, RGB.max_value)
        green = random.randint(RGB.min_value, RGB.max_value)
        blue = random.randint(RGB.min_value, RGB.max_value)
        alpha = random.uniform(RGB.min_value, RGB.max_alpha_value)
        return RGB(red, green, blue, alpha)


class HSV:

    def __init__(self, hue, saturation, value, alpha=1):
        self.hue = hue
        self.saturation = saturation
        self.value = value
        self.alpha = alpha

    def output_to_string(self):
        to_return = f'hsv({self.hue}, {self.saturation}%, {self.value}%)'
        return to_return

    def output_hsv_with_alpha(self):
        to_return = (self.hue, self.saturation, self.value, self.alpha)
        return to_return

    def to_rgb(self):

        hue = self.hue
        saturation = self.saturation / 100
        value = self.value / 100

        c = saturation * value
        x = c * (1 - abs(((hue / 60) % 2) - 1))
        m = value - c

        if 0 <= hue < 60:
            r, g, b = c, x, 0
        elif 60 <= hue < 120:
            r, g, b = x, c, 0
        elif 120 <= hue < 180:
            r, g, b = 0, c, x
        elif 180 <= hue < 240:
            r, g, b = 0, x, c
        elif 240 <= hue < 300:
            r, g, b = x, 0, c
        elif 300 <= hue < 360:
            r, g, b = c, 0, x

        red = round((r + m) * 255)
        green = round((g + m) * 255)
        blue = round((b + m) * 255)

        return RGB(red, green, blue, self.alpha)
