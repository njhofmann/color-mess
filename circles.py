from PIL import Image, ImageDraw
import random
import colorsys
import math
import copy


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


def create_color_static(wid, hgt):
    pixels = []

    for pixel in range(wid * hgt):
        temp = RGB.create_random_rgb()
        to_add = (temp.red, temp.green, temp.blue)
        pixels.append(to_add)

    to_render = Image.new('RGB', (wid, hgt))
    to_render.putdata(pixels)
    return to_render


def linear_interpolation_at_t(start, end, t):
    return start + ((end - start) * t)


def x_colors_gradient_over_n(list_of_colors, n, hsv=False):
    x = len(list_of_colors)

    if n <= x - 1:
        raise ValueError('')

    if x == 1:
        return [copy.copy(list_of_colors[0]) for i in range(n)]

    pairs = []
    for i in range(x - 1):
        a = list_of_colors[i]
        b = list_of_colors[i + 1]
        key = (a, b)
        pairs.append(key)

    base, overhang = divmod(n - 1, x - 1)

    def rounded_value_at_t(start, end, t):
        return round(start + ((end - start) * t))

    gradient_values = []
    for idx, pair in enumerate(pairs):
        temp = base

        if overhang > 0:
            temp += 1
            overhang -= 1

        a = pair[0]
        b = pair[1]
        for i in range(temp):
            t = i / temp

            if hsv:
                hsv_a = a.to_hsv()
                hsv_b = b.to_hsv()

                to_add_hue = rounded_value_at_t(hsv_a.hue, hsv_b.hue, t)
                to_add_saturation = rounded_value_at_t(hsv_a.saturation, hsv_b.saturation, t)
                to_add_value = rounded_value_at_t(hsv_a.value, hsv_b.value, t)
                to_add = HSV(to_add_hue, to_add_saturation, to_add_value)
                to_add = to_add.to_rgb()
            else:
                to_add_red = rounded_value_at_t(a.red, b.red, t)
                to_add_green = rounded_value_at_t(a.green, b.green, t)
                to_add_blue = rounded_value_at_t(a.blue, b.blue, t)
                to_add = RGB(to_add_red, to_add_green, to_add_blue)

            gradient_values.append(to_add.output_rgb())

            if idx == len(pairs) - 1 and i == temp - 1:
                gradient_values.append(b.output_rgb())

    return gradient_values


def rect_gradient(list_of_colors, width, height, hsv=False):
    results = x_colors_gradient_over_n(list_of_colors, width, hsv)

    to_render = Image.new('RGB', (width, height))
    to_draw = ImageDraw.Draw(to_render)

    for idx, color in enumerate(results):
        to_draw.line([idx, 0, idx, height - 1], color, 0)

    return to_render


def square_gradient(list_of_colors, length, hsv=False):
    radius = int(math.floor(length / 2))
    if len(colors) > radius:
        raise ValueError('')

    gradient_values = x_colors_gradient_over_n(list_of_colors, radius, hsv)

    to_render = Image.new('RGB', (length, length), (255, 255, 255))
    to_draw = ImageDraw.Draw(to_render)

    x0 = radius - 1
    x1 = x0 + 1
    for i in range(radius):
        to_draw.rectangle([x0, x0, x1, x1], outline=gradient_values[i])
        print(x0, x1)
        x0 -= 1
        x1 += 1
    return to_render


a = RGB(255, 255, 0)
b = RGB(153, 76, 0)
c = RGB(0, 0, 204)
colors = [a, b, c]
img = square_gradient(colors, 5000, False)
img.show()

