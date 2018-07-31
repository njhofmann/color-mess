from PIL import Image, ImageDraw
import math
import copy
from src import RGB, HSV


def create_color_static(wid, hgt):
    pixels = []

    for pixel in range(wid * hgt):
        temp = RGB.create_random_rgb()
        to_add = (temp.red, temp.green, temp.blue)
        pixels.append(to_add)

    to_render = Image.new('RGB', (wid, hgt))
    to_render.putdata(pixels)
    return to_render


def gradient_of_x_colors_over_n(list_of_colors, n, hsv=False):
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


def line_gradient(list_of_colors, width, height, hsv=False):
    results = gradient_of_x_colors_over_n(list_of_colors, width, hsv)

    to_render = Image.new('RGB', (width, height))
    to_draw = ImageDraw.Draw(to_render)

    for idx, color in enumerate(results):
        to_draw.line([idx, 0, idx, height - 1], color, 0)

    return to_render


def square_gradient(list_of_colors, length, hsv=False):
    radius = math.ceil(length / 2)

    if len(list_of_colors) > radius:
        raise ValueError('')

    gradient_values = gradient_of_x_colors_over_n(list_of_colors, radius, hsv)

    to_render = Image.new('RGB', (length, length), (255, 255, 255))
    to_draw = ImageDraw.Draw(to_render)

    x0 = radius - 1
    x1 = x0 + 1
    for i in range(radius):
        to_draw.rectangle([x0, x0, x1, x1], outline=gradient_values[i])
        x0 -= 1
        x1 += 1

    return to_render


def rect_gradient(list_of_colors, width, height, hsv=False):
    if width < height:
        shorter_radius = math.ceil(width / 2)
        longer_radius = math.ceil(height / 2)
        to_render = Image.new('RGB', (height, width), (255, 255, 255))
    elif width > height:
        shorter_radius = math.ceil(height / 2)
        longer_radius = math.ceil(width / 2)
        to_render = Image.new('RGB', (width, height), (255, 255, 255))
    else:
        return square_gradient(list_of_colors, width, hsv)

    to_draw = ImageDraw.Draw(to_render)
    gradient_values = gradient_of_x_colors_over_n(list_of_colors, shorter_radius, hsv)
    ratio = shorter_radius / longer_radius

    x0 = longer_radius
    y0 = shorter_radius
    x1 = x0 + 1
    y1 = y0 + 1

    for i in range(longer_radius + 1):
        cur_value = shorter_radius - y0
        if cur_value >= len(gradient_values):
            cur_value -= 1

        to_draw.rectangle([x0, y0, x1, y1], outline=gradient_values[cur_value])

        x0 -= 1
        y0 = round(ratio * x0)
        x1 += 1
        y1 = round(ratio * x1)

    if width < height:
        return to_render.rotate(90, expand=True)

    return to_render


def circle_gradient(list_of_colors, radius):
    gradient_values = gradient_of_x_colors_over_n(list_of_colors, radius)

    diameter = 2 * radius
    to_render = Image.new('RGB', (diameter, diameter), (255, 255, 255))
    to_draw = ImageDraw.Draw(to_render)

    for i in range(radius):
        b = diameter - i - 1
        to_draw.ellipse([i, i, b , b], fill=gradient_values[radius - i - 1])

    return to_render


a = RGB(255, 0, 0)
b = RGB(56, 98, 245)
c = RGB(98, 0, 123)
colors = [a, b, c]
img = circle_gradient(colors, 1000)
img.show()

