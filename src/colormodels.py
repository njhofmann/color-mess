import random

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
min_value = 0
rgb_max_value = 255
alpha_max = 100


class RGB:

    def __init__(self, red, green, blue, alpha=alpha_max):
        if not (min_value <= red <= rgb_max_value):
            raise ValueError('Red value must be in range [0, 255]!')
        elif not (min_value <= green <= rgb_max_value):
            raise ValueError('Green value must be in range [0, 255]!')
        elif not (min_value <= blue <= rgb_max_value):
            raise ValueError('Blue value must be in range [0, 255]!')
        elif not (min_value <= alpha <= alpha_max):
            raise ValueError('Alpha value must be in range [0, 100]!')

        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def output(self):
        red = round(self.red)
        green = round(self.green)
        blue = round(self.blue)
        return red, green, blue

    def output_as_rgba(self):
        red = round(self.red)
        green = round(self.green)
        blue = round(self.blue)
        return red, green, blue, self.alpha

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

        to_return = HSV(hue, saturation, value, self.alpha)

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
                return var ** (1/3)
            else:
                return (var * 7.787) + (16 / 116)

        x = lab_mid_transform(x)
        y = lab_mid_transform(y)
        z = lab_mid_transform(z)

        light = (116 * y) - 16
        a = 500 * (x - y)
        b = 200 * (y - z)

        if light <= 0:
            light = 0
        elif 100 <= light:
            light = 100

        return LAB(light, a, b, self.alpha)

    @staticmethod
    def random_rgb():
        red = random.randint(min_value, rgb_max_value)
        green = random.randint(min_value, rgb_max_value)
        blue = random.randint(min_value, rgb_max_value)
        return RGB(red, green, blue)

    @staticmethod
    def n_random_rbgs(n):
        if n < 2:
            raise ValueError('n must be >= 2!')

        to_return = []
        for i in range(n):
            to_return.append(RGB.random_rgb())
        return to_return

    @staticmethod
    def n_random_rgba(n):
        rgbas = RGB.n_random_rbgs(n)
        cur_alpha = alpha_max
        increment = cur_alpha / (n - 1)

        for i in range(n):
            rgbas[i].alpha = cur_alpha
            cur_alpha -= increment

        rgbas[len(rgbas) - 1].alpha = 0

        return rgbas



class HSV:
    max_hue = 360
    max_sv = 100

    def __init__(self, hue, saturation, value, alpha=alpha_max):
        if not (min_value <= hue <= HSV.max_hue):
            raise ValueError('Hue must be in range [0, 360]')
        elif not (min_value <= saturation <= HSV.max_sv):
            raise ValueError('Saturation must be in range [0, 100]!')
        elif not (min_value <= value <= HSV.max_sv):
            raise ValueError('Value must be in range [0, 100]!')
        elif not (min_value <= alpha <= alpha_max):
            raise ValueError('Alpha value must be in range [0, 1]!')

        # For testing purposes due to information lose when converting to other color formats
        if hue == 360:  #
            self.hue = 0
        else:
            self.hue = hue

        self.saturation = saturation
        self.value = value
        self.alpha = alpha

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

        red = (r + m) * rgb_max_value
        green = ((g + m) * rgb_max_value)
        blue = ((b + m) * rgb_max_value)

        return RGB(red, green, blue, self.alpha)

    def to_lab(self):
        rgb = self.to_rgb()
        to_return = rgb.to_lab()
        return to_return

    @staticmethod
    def random_hsv():
        hue = random.randint(min_value, HSV.max_hue)
        saturation = random.randint(min_value, HSV.max_sv)
        value = random.randint(min_value, HSV.max_sv)
        return HSV(hue, saturation, value)


class LAB:
    max_light = 100

    def __init__(self, light, a, b, alpha=alpha_max):
        if not (min_value <= light <= LAB.max_light):
            raise ValueError('Light must in range [0, 100]!')
        elif not (min_value <= alpha <= alpha_max):
            raise ValueError('Alpha value must be in range [0, 1]!')

        self.light = light
        self.a = a
        self.b = b
        self.alpha = alpha

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

            var *= rgb_max_value

            return var

        red = rgb_transform(red)
        green = rgb_transform(green)
        blue = rgb_transform(blue)

        if red <= 0:
            red = 0
        elif rgb_max_value <= red:
            red = rgb_max_value

        if green <= 0:
            green = 0
        elif rgb_max_value <= green:
            green = rgb_max_value

        if blue <= 0:
            blue = 0
        elif rgb_max_value <= blue:
            blue = rgb_max_value

        return RGB(red, green, blue, self.alpha)

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
