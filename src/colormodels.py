import colorsys
import random

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

        hsv = colorsys.rgb_to_hsv(red, green, blue)

        hue = hsv[0] * 360
        saturation = hsv[1] * 100
        value = hsv[2] * 100

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
        hue = self.hue / 360
        saturation = self.saturation / 100
        value = self.value / 100

        rgb = colorsys.hsv_to_rgb(hue, saturation, value)

        red = round(rgb[0] * 255)
        green = round(rgb[1] * 255)
        blue = round(rgb[2] * 255)

        return RGB(red, green, blue, self.alpha)