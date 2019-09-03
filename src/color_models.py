import random

"""
Set of colors models for the RGB, HSV, and LAB color spaces.
"""

'''
The conversion between an RGB value to a LAB value is not one to one, each conversion requires an intermediary 
transformation to the XYZ color space, the XYZ color space depends on a specific illumination with its own set of 
reference values and transformation variables. This model is built using the D65/2° standard illumination. References
values are given below, transformation variables are marked in the respective methods.
'''

ref_x = 95.047
ref_y = 100
ref_z = 108.883

ROUNDING_ERROR = 4  # If a color space is to output a decimal, determines to what place that output should be to at max
MIN_VALUE = 0  # Minimum value for any color component, including alpha.
MAX_RGB = 255
MAX_ALPHA = 100  # Default and maximum alpha value


class RGB:
    """
    Represents a color in the RGB space.
    """

    def __init__(self, red: int, green: int, blue: int, alpha: int =MAX_ALPHA):
        """
        Constructs a RGB object from a given red, green, and blue (and optional alpha) components.
        :param red: red value to set for this RGB
        :param green: green value for this RGB
        :param blue: blue value for this RGB
        :param alpha: optional alpha composite value for this RGB object
        :raise: if any of the given values are outside their respective ranges
        """
        if not (MIN_VALUE <= red <= MAX_RGB):
            raise ValueError('Red value must be in range [0, 255]!')
        elif not (MIN_VALUE <= green <= MAX_RGB):
            raise ValueError('Green value must be in range [0, 255]!')
        elif not (MIN_VALUE <= blue <= MAX_RGB):
            raise ValueError('Blue value must be in range [0, 255]!')
        elif not (MIN_VALUE <= alpha <= MAX_ALPHA):
            raise ValueError('Alpha value must be in range [0, 100]!')

        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def output(self):
        """
        Returns the individual red, green, and blue components of this RGB as a tuple - rounded to nearest int.
        :return: tuple of this RGB's individual components (minus alpha)
        """
        red = round(self.red)
        green = round(self.green)
        blue = round(self.blue)
        return red, green, blue

    def output_as_rgba(self):
        """
        Returns the individual red, green, blue, and alpha components of this RGB as a tuple - rounded to nearest int.
        :return: tuple of this RGB's individual components (with alpha)
        """
        red = round(self.red)
        green = round(self.green)
        blue = round(self.blue)
        return red, green, blue, self.alpha

    def same_color(self, other):
        """
        Returns if this RGB represents the same color as another given RGB, HSV, or LAB object.
        :param other: other color to compare to
        :return: if this color and given color are the same
        :raise: if given input is not of the type RGB, HSV, or LAB
        """
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
        """
        Converts this RGB to an equivalent HSV object representing the same color.
        :return: HSV object representing same color as this RGB
        """
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
        """
        Converts this RGB to an equivalent LAB object representing the same color.
        :return: LAB object representing same color as this RGB
        """
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
        """
        Creates a RGB object representing a random color
        :return: random RGB object
        """
        red = random.randint(MIN_VALUE, MAX_RGB)
        green = random.randint(MIN_VALUE, MAX_RGB)
        blue = random.randint(MIN_VALUE, MAX_RGB)
        return RGB(red, green, blue)

    @staticmethod
    def n_random_rbg(n=random.randint(3, 8)):
        """
        Returns a list of n randomly generated RGB objects.
        :param n: number of RGB objects to create
        :return: list of n random RGB objects
        :raise: if given n is less than 1
        """
        if n < 1:
            raise ValueError('n must be >= 1!')

        to_return = []
        for i in range(n):
            to_return.append(RGB.random_rgb())
        return to_return

    @staticmethod
    def n_random_rgba(n):
        """
        Returns a list of n randomly generated RGB objects with random alpha values as well.
        :param n: number of RGB objects to create
        :return: list of n random RGB objects
        :raise: if given n is less than 1
        """
        rgbas = RGB.n_random_rbg(n)
        cur_alpha = MAX_ALPHA
        increment = cur_alpha / (n - 1)

        for i in range(n):
            rgbas[i].alpha = cur_alpha
            cur_alpha -= increment

        rgbas[len(rgbas) - 1].alpha = 0

        return rgbas


class HSV:
    """
    Represents a color in the HSV color space.
    """
    max_hue = 360
    max_sv = 100

    def __init__(self, hue: int, saturation: int, value:int, alpha: int =MAX_ALPHA):
        """
        Creates a HSV object from a given hue, saturation, and value (and optional alpha composite) values.
        :param hue: hue value for this HSV object
        :param saturation: saturation value for this HSV object
        :param value: value value for this HSV object
        :param alpha: optional alpha composite value for this HSV object
        :raise: if any of the given values are outside their respective ranges
        """
        if not (MIN_VALUE <= hue <= HSV.max_hue):
            raise ValueError('Hue must be in range [0, 360]')
        elif not (MIN_VALUE <= saturation <= HSV.max_sv):
            raise ValueError('Saturation must be in range [0, 100]!')
        elif not (MIN_VALUE <= value <= HSV.max_sv):
            raise ValueError('Value must be in range [0, 100]!')
        elif not (MIN_VALUE <= alpha <= MAX_ALPHA):
            raise ValueError('Alpha value must be in range [0, 1]!')

        # In place due to information lose when converting to other color formats
        if hue == 360:  #
            self.hue = 0
        else:
            self.hue = hue

        self.saturation = saturation
        self.value = value
        self.alpha = alpha

    def output(self):
        """
        Returns the individual hue, saturation, and value components of this HSV as a tuple - rounded to nearest int.
        :return: tuple of this HSV's individual components (minus alpha)
        """
        hue = round(self.hue)
        saturation = round(self.saturation)
        value = round(self.value)
        return hue, saturation, value

    def output_to_string(self):
        """
        Returns the individual hue, saturation, and value components of this HSV as a formatted string - rounded to
        nearest int. Meant to be used with the extra HSV string parameter for RGB in PILLOW.
        :return: string of this HSV's individual components (minus alpha)
        """
        hue = round(self.hue, ROUNDING_ERROR)
        saturation = round(self.saturation, ROUNDING_ERROR)
        value = round(self.value, ROUNDING_ERROR)
        return f'hsv({hue}, {saturation}%, {value}%)'

    def same_color(self, other):
        """
        Returns if this HSV represents the same color as another given RGB, HSV, or LAB object.
        :param other: other color to compare to
        :return: if this color and given color are the same
        :raise: if given input is not of the type RGB, HSV, or LAB
        """
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
        """
        Converts this HSV to an equivalent RGB object representing the same color.
        :return: RGB object representing same color as this HSV
        """
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

        red = (r + m) * MAX_RGB
        green = ((g + m) * MAX_RGB)
        blue = ((b + m) * MAX_RGB)

        if red > 255:
            red = 255
        elif red < 0:
            red = 0

        if green > 255:
            green = 255
        elif green < 0:
            green = 0

        if blue > 255:
            blue = 255
        elif blue < 0:
            blue = 0

        return RGB(red, green, blue, self.alpha)

    def to_lab(self):
        """
        Converts this HSV to an equivalent LAB object representing the same color.
        :return: LAB object representing same color as this HSV
        """
        rgb = self.to_rgb()
        to_return = rgb.to_lab()
        return to_return

    @staticmethod
    def random_hsv():
        """
        Creates a HSV object representing a random color
        :return: random HSV object
        """
        hue = random.randint(MIN_VALUE, HSV.max_hue)
        saturation = random.randint(MIN_VALUE, HSV.max_sv)
        value = random.randint(MIN_VALUE, HSV.max_sv)
        return HSV(hue, saturation, value)


class LAB:
    """
    Represents a color in the LAB color space.
    """
    max_light = 100

    def __init__(self, light: int, a: int, b: int, alpha: int =MAX_ALPHA):
        """

        :param light: light value for this LAB
        :param a: a value for this lab
        :param b: b value for this lab
        :param alpha: optional alpha composite value for this LAB
        :raise: if any of the given values are outside their respective ranges
        """
        if not (MIN_VALUE <= light <= LAB.max_light):
            raise ValueError('Light must in range [0, 100]!')
        elif not (MIN_VALUE <= alpha <= MAX_ALPHA):
            raise ValueError('Alpha value must be in range [0, 1]!')

        self.light = light
        self.a = a
        self.b = b
        self.alpha = alpha

    def output(self):
        """
        Returns the individual light, a, and b components of this LAB as a tuple - rounded to nearest int.
        :return: tuple of this LAB's individual components (minus alpha)
        """
        light = round(self.light)
        a = round(self.a)
        b = round(self.b)
        return light, a, b

    def same_color(self, other):
        """
        Returns if this LAB represents the same color as another given RGB, HSV, or LAB object.
        :param other: other color to compare to
        :return: if this color and given color are the same
        :raise: if given input is not of the type RGB, HSV, or LAB
        """
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
        """
        Converts this LAB to an equivalent RGB object representing the same color.
        :return: RGB object representing same color as this LAB
        """
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
            """

            :param var:
            :return:
            """
            if var > .0031308:
                var = 1.055 * (var ** (1 / 2.4)) - .055
            else:
                var *= 12.92

            var *= MAX_RGB

            return var

        red = rgb_transform(red)
        green = rgb_transform(green)
        blue = rgb_transform(blue)

        if red <= 0:
            red = 0
        elif MAX_RGB <= red:
            red = MAX_RGB

        if green <= 0:
            green = 0
        elif MAX_RGB <= green:
            green = MAX_RGB

        if blue <= 0:
            blue = 0
        elif MAX_RGB <= blue:
            blue = MAX_RGB

        return RGB(red, green, blue, self.alpha)

    def to_hsv(self):
        """
        Converts this LAB to an equivalent HSV object representing the same color.
        :return: HSV object representing same color as this LAB
        """
        rgb = self.to_rgb()
        to_return = rgb.to_hsv()
        return to_return

    @staticmethod
    def random_lab():
        """
        Creates a LAB object representing a random color
        :return: random LAB object
        """
        a_b_range = 128
        light = random.randint(LAB.min_light, LAB.max_light)
        a = random.randint(-a_b_range, a_b_range)
        b = random.randint(-a_b_range, a_b_range)
        return LAB(light, a, b)
