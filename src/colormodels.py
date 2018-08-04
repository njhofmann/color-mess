import colorsys
import random
import math

'''
The conversion between an RGB value to a LAB value is not one to one, each conversion requires an intermediary 
transformation to the XYZ color space, the XYZ color space depends on a specific illumination with its own set of 
reference values and transformation variables. This model is built using the D65/2° standard illumination. References
values are given below, transformation variables are marked in the respective methods.
'''
ref_x = 95.047
ref_y = 100
ref_z = 108.883

# If a color space is to output a decimal, determines to what place that output should be to at max
round_to = 4


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
        red = round(self.red)
        green = round(self.green)
        blue = round(self.blue)
        return red, green, blue

    def same_color(self, other):
        def same_attributes(temp):
            return self.output() == temp.output()

        if isinstance(other, RGB):
            return same_attributes(other)
        elif isinstance(other, HSV):
            rgb = other.to_rgb()
            return same_attributes(rgb)
        elif isinstance(other, LAB):
            rgb = other.to_rgb()
            return same_attributes(rgb)
        else:
            raise TypeError('Given input isn\'t a color of type RGb, HSV, or LAB!')

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

        to_return = HSV(hue, saturation, value)

        return to_return

    def to_lab(self):
        red = self.red / 255.0
        green = self.green / 255.0
        blue = self.blue / 255.0

        def xyz_mid_transform(var):
            if var > .04045:
                var = (((var + .055) / 1.055) ** 2.4)
            else:
                var /= 12.92

            var *= 100.0

            return var

        red = xyz_mid_transform(red)
        green = xyz_mid_transform(green)
        blue = xyz_mid_transform(blue)

        # RGB -> XYZ transformation variables
        x = ((red * .4124564) + (green * .3575761) + (blue * .1804375)) / ref_x
        y = ((red * .2126729) + (green * .7151522) + (blue * .0721750)) / ref_y
        z = ((red * .0193339) + (green * .1191920) + (blue * .9503041)) / ref_z

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

        # For testing purposes due to information lose when converting to other color formats
        if hue == 360:  #
            self.hue = 0
            self.saturation = saturation
            self.value = value
        else:
            self.hue = hue
            self.saturation = saturation
            self.value = value

    def output(self):
        hue = round(self.hue)
        saturation = round(self.saturation)
        value = round(self.value)
        return hue, saturation, value

    def output_to_string(self):
        hue = round(self.hue, round_to)
        saturation = round(self.saturation, round_to)
        value = round(self.value, round_to)
        return f'hsv({hue}, {saturation}%, {value}%)'

    def same_color(self, other):
        def same_attributes(temp):
            a = self.output()
            b = temp.output()

            if a[2] == 0 and b[2] == 0:  # If their values are both zero, they are both black - hue and saturation
                return True              # don't matter.
            elif a[1] == 0 and b[1] == 0:  # If saturations are both zero, only thing to check is their values.
                return a[2] == b[2]
            else:
                return a == b

        if isinstance(other, HSV):
            return same_attributes(other)
        elif isinstance(other, RGB):
            hsv = other.to_hsv()
            return same_attributes(hsv)
        elif isinstance(other, LAB):
            hsv = other.to_hsv()
            return same_attributes(hsv)
        else:
            raise TypeError('Given input isn\'t a color of type RGB, HSV, or LAB!')


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
        else:
            r, g, b = c, 0, x

        red = (r + m) * 255
        green = ((g + m) * 255)
        blue = ((b + m) * 255)

        return RGB(red, green, blue)

    def to_lab(self):
        rgb = self.to_rgb()
        to_return = rgb.to_lab()
        return to_return

    @staticmethod
    def random_hsv():
        hue = random.randint(HSV.min_value, HSV.max_hue)
        saturation = random.randint(HSV.min_value, HSV.max_sv)
        value = random.randint(HSV.min_value, HSV.max_sv)
        return HSV(hue, saturation, value)


class LAB:
    max_light = 100
    min_light = 0

    def __init__(self, light, a, b):
        if not (LAB.min_light <= light <= LAB.max_light):
            raise ValueError('Light must in range [0, 100]!')

        self.light = light
        self.a = a
        self.b = b

    def output(self):
        light = round(self.light)
        a = round(self.a)
        b = round(self.b)
        return light, a, b

    def same_color(self, other):
        def same_attributes(temp):
            return self.output() == temp.output()

        if isinstance(other, LAB):
            return same_attributes(other)
        elif isinstance(other, RGB):
            lab = other.to_lab()
            return same_attributes(lab)
        elif isinstance(other, HSV):
            lab = other.to_lab()
            return same_attributes(lab)
        else:
            raise TypeError('Given input isn\'t a color of type RGB, HSV, or LAB!')

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

        x = xyz_transform(x) * ref_x
        y = xyz_transform(y) * ref_y
        z = xyz_transform(z) * ref_z

        x /= 100
        y /= 100
        z /= 100

        # XYZ -> RGB transformation variables
        red = (x * 3.2404542) + (y * -1.5371385) + (z * -.4985314)
        green = (x * -.9692660) + (y * 1.8760108) + (z * .0415560)
        blue = (x * .0556434) + (y * -.2040259) + (z * 1.0572252)

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

        if red < 0:
            red = 0
        elif 255 < red:
            red = 255
        elif green < 0:
            green = 0
        elif 255 < green:
            green = 255
        elif blue < 0:
            blue = 0
        elif 255 < blue:
            blue = 255

        return RGB(red, green, blue)

    def to_hsv(self):
        rgb = self.to_rgb()
        to_return = rgb.to_hsv()
        return to_return

    @staticmethod
    def random_lab():
        a_b_range = 128
        light = random.randint(LAB.min_light, LAB.max_light)
        a = random.randint(-a_b_range, a_b_range)
        b = random.randint(-a_b_range, a_b_range)
        return LAB(light, a, b)
