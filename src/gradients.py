from PIL import Image, ImageDraw
import copy
from src import *


'''
Every gradient can be created in either the RGB, RGBA, HSV, or LAB color spaces.
To display a gradient in the desired mode, set the optional 'mode' parameter to the following, RGB by default:
-RGB - 'rgb' 
-RGBA - 'rgba'
-HSV - 'hsv'
-LAB - 'lab'
'''


def create_color_static(wid, hgt):
    pixels = []

    for pixel in range(wid * hgt):
        temp = RGB.random_rgb()
        to_add = (temp.red, temp.green, temp.blue)
        pixels.append(to_add)

    to_render = Image.new('RGB', (wid, hgt))
    to_render.putdata(pixels)
    return to_render


def rectangle(image, coordinates, cur_color):
    to_draw = ImageDraw.Draw(image)
    to_draw.rectangle(coordinates, fill=cur_color)


def ellipse(image, coordinates, cur_color):
    to_draw = ImageDraw.Draw(image)
    to_draw.ellipse(coordinates, fill=cur_color)


def diamond(image, coordinates, cur_color, vert, horz):
    x0 = coordinates[0]
    y0 = coordinates[1]
    x1 = coordinates[2]
    y1 = coordinates[3]

    horz_b = 1 - horz

    a = (x0, y0 + (vert * (y1 - y0)))
    b = ((horz_b * (x1 - x0)) + x0, y0)
    c = ((horz * (x1 - x0)) + x0, y0)
    d = (x1, y0 + (vert * (y1 - y0)))
    e = (((x1 - x0) / 2) + x0, y1)

    coordinates = [a, b, c, d, e]
    to_draw = ImageDraw.Draw(image)
    to_draw.polygon(coordinates, fill=cur_color)


def gradient_of_x_colors_over_n(list_of_colors, n, mode='rgb', alpha=False):
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

            if mode == 'hsv':
                hsv_a = a.to_hsv()
                hsv_b = b.to_hsv()

                to_add_hue = rounded_value_at_t(hsv_a.hue, hsv_b.hue, t)
                to_add_saturation = rounded_value_at_t(hsv_a.saturation, hsv_b.saturation, t)
                to_add_value = rounded_value_at_t(hsv_a.value, hsv_b.value, t)
                to_add = HSV(to_add_hue, to_add_saturation, to_add_value)
                to_add = to_add.to_rgb()
            elif mode == 'lab':
                lab_a = a.to_lab()
                lab_b = b.to_lab()
                
                to_add_light = rounded_value_at_t(lab_a.light, lab_b.light, t)
                to_add_a = rounded_value_at_t(lab_a.a, lab_b.a, t)
                to_add_b = rounded_value_at_t(lab_a.b, lab_b.b, t)
                to_add = LAB(to_add_light, to_add_a, to_add_b)
                to_add = to_add.to_rgb()
            elif mode == 'rgb':
                to_add_red = rounded_value_at_t(a.red, b.red, t)
                to_add_green = rounded_value_at_t(a.green, b.green, t)
                to_add_blue = rounded_value_at_t(a.blue, b.blue, t)
                to_add = RGB(to_add_red, to_add_green, to_add_blue)
            else:
                raise ValueError('Invalid color space!')

            if alpha:
                to_add.alpha = rounded_value_at_t(a.alpha, b.alpha, t)
                gradient_values.append(to_add.output_as_rgba())
            else:
                gradient_values.append(to_add.output())

            if idx == len(pairs) - 1 and i == temp - 1:
                if mode == 'rgba':
                    gradient_values.append(b.output_as_rgba())
                else:
                    gradient_values.append(b.output())

    return gradient_values


def line_gradient(list_of_colors, width, height, mode='rgb', alpha=False):
    results = gradient_of_x_colors_over_n(list_of_colors, width, mode, alpha)

    if alpha:
        to_render = Image.new('RGBA', (width, height))
    else:
        to_render = Image.new('RGB', (width, height))
    to_draw = ImageDraw.Draw(to_render)

    for idx, color in enumerate(results):
        to_draw.line([idx, 0, idx, height - 1], color, 0)

    return to_render


def even_diamond_gradient(list_of_colors, width, height, fill_background=False, mode='rgb', alpha=False):
    def even_diamond(image, coordinates, cur_color):
        even = .5
        return diamond(image, coordinates, cur_color, even, even)

    return master_gradient(list_of_colors, width, height, even_diamond, fill_background, mode, alpha)


def diamond_gradient(list_of_colors, width, height, fill_background=False, mode='rgb', alpha=False):
    def diamond_jewel(image, coordinates, cur_color):
        return diamond(image, coordinates, cur_color, .25, .75)

    return master_gradient(list_of_colors, width, height, diamond_jewel, fill_background, mode, alpha)


def square_gradient(list_of_colors, length, fill_background=False, mode='rgb', alpha=False):
    return master_gradient(list_of_colors, length, length, rectangle, fill_background, mode, alpha)


def rectangle_gradient(list_of_colors, width, height,fill_background=False,  mode='rgb', alpha=False):
    return master_gradient(list_of_colors, width, height, rectangle, fill_background, mode, alpha)


def circle_gradient(list_of_colors, radius, fill_background=False, mode='rgb', alpha=False):
    return master_gradient(list_of_colors, radius * 2, radius * 2, ellipse, fill_background, mode)


def ellipse_gradient(list_of_colors, x_radius, y_radius, fill_background=False, mode='rgb'):
    return master_gradient(list_of_colors, x_radius * 2, y_radius * 2, ellipse, fill_background, mode)


def master_gradient(list_of_colors, width, height, shape, fill_background=False, mode='rgb', alpha=False):
    if width <= height:
        shorter_radius = math.ceil(width / 2)
        longer_radius = math.ceil(height / 2)
    else:
        shorter_radius = math.ceil(height / 2)
        longer_radius = math.ceil(width / 2)

    size = (width, height)
    gradient_values = gradient_of_x_colors_over_n(list_of_colors, longer_radius, mode, alpha)
    ratio = shorter_radius / longer_radius

    if alpha:
        to_render = Image.new('RGBA', size, (255, 255, 255, 0))
    else:
        to_render = Image.new('RGB', size, (255, 255, 255))

    if fill_background:
        to_render.paste(gradient_values[-1], [0, 0, to_render.size[0], to_render.size[1]])

    x0 = 0
    y0 = 0
    x1 = to_render.width
    y1 = to_render.height

    for i in range(longer_radius):
        coordinates = [x0, y0, x1, y1]
        cur_color = gradient_values[longer_radius - i - 1]
        shape(to_render, coordinates, cur_color)

        if width <= height:
            y0 += 1
            x0 = round(y0 * ratio)
        else:
            x0 += 1
            y0 = round(x0 * ratio)

        x1 = to_render.width - x0
        y1 = to_render.height - y0

    return to_render