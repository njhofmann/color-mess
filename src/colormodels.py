import colorsys
import random
import math


class RGB:
    min_value = 0
    max_value = 255
    alpha_max = 1

    def __init__(self, red, green, blue):
        if (not (RGB.min_value <= red <= RGB.max_value)) \
                or (not (RGB.min_value <= green <= RGB.max_value)) \
                or (not (RGB.min_value <= blue <= RGB.max_value)):
            raise ValueError('RGB values must be ints in range [0, 255]!')

        self.red = red
        self.green = green
        self.blue = blue

    def output(self):
        to_return = (self.red, self.green, self.blue)
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

        return HSV(hue, saturation, value)

    def to_lab(self):
        red = self.red / 255.0
        green = self.green / 255.0
        blue = self.blue / 255.0

        def xyz_mid_transform(var):
            if var > 0.04045:
                var = (((var + 0.055) / 1.055) ** 2.4)
            else:
                var /= 12.92

            var *= 100.0

            return var

        red = xyz_mid_transform(red)
        green = xyz_mid_transform(green)
        blue = xyz_mid_transform(blue)

        x = ((red * .4124564) + (green * .3575761) + (blue * .1804375))
        y = ((red * .2126729) + (green * .7151522) + (blue * .0721750))
        z = ((red * .0193339) + (green * .1191920) + (blue * .9503041))

        x /= 95.047
        y /= 100
        z /= 108.883

        def lab_mid_transform(var):
            if var > .008856:
                var **= (1/3)
            else:
                var = (var * 7.787) + (16 / 116)

            return var

        x = lab_mid_transform(x)
        y = lab_mid_transform(y)
        z = lab_mid_transform(z)

        light = (116 * y) - 16
        a = 500 * (x - y)
        b = 200 * (y - z)

        return LAB(light, a, b)


    @staticmethod
    def random_rgb():
        red = random.randint(RGB.min_value, RGB.max_value)
        green = random.randint(RGB.min_value, RGB.max_value)
        blue = random.randint(RGB.min_value, RGB.max_value)
        return RGB(red, green, blue)


class HSV:
    min_value = 0
    max_hue = 360
    max_sv = 100

    def __init__(self, hue, saturation, value):
        if not (HSV.min_value <= hue <= HSV.max_hue):
            raise ValueError('Hue must be in range [0, 360]')
        elif not (HSV.min_value <= saturation <= HSV.max_sv):
            raise ValueError('Saturation must be in range [0, 100]!')
        elif not (HSV.min_value <= value <= HSV.max_sv):
            raise ValueError('Value must be in range [0, 100]!')

        self.hue = hue
        self.saturation = saturation
        self.value = value

    def output(self):
        to_return = (self.hue, self.saturation, self.value)
        return to_return

    def output_to_string(self):
        to_return = f'hsv({self.hue}, {self.saturation}%, {self.value}%)'
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

        return RGB(red, green, blue)

    def to_lab(self):
        rgb = self.to_rgb()
        return rgb.to_lab()


class LAB:

    def __init__(self, light, a, b):
        if not (0 <= light <= 100):
            raise ValueError('Light must in range [0, 100]!')

        self.light = light
        self.a = a
        self.b = b

    def output(self):
        to_return = (self.light, self.a, self.b)
        return to_return

    def to_rgb(self):
        y = (self.light + 16) / 116
        x = (self.a / 500) + y
        z = y - (self.b / 200)

        def xyz_transform(var):
            if (var ** 3) > .008856:
                var **= 3
            else:
                var = (var - 16 / 116) / 7.787

            return var

        x = xyz_transform(x)
        y = xyz_transform(y)
        z = xyz_transform(z)

        x *= 95.047
        y *= 100
        z *= 108.883

        x /= 100
        y /= 100
        z /= 100

        red = (x * 3.2404542) + (y * -1.5371385) + (z * -.4985314)
        green = (x * -.9692660) + (y * 1.8760108) + (z * .0415560)
        blue = (x * .0556434) + (y * .2040259) + (z * 1.0572252)

        def rgb_transform(var):
            if var > .0031308:
                var = 1.055 * (var ** (1 / 2.4)) - .055
            else:
                var *= 12.92

            var *= 255

            return var

        red = rgb_transform(red)
        green = rgb_transform(green)
        blue = rgb_transform(blue)

        return RGB(red, green, blue)

    def to_hsv(self):
        rgb = self.to_rgb()
        return rgb.to_hsv()
