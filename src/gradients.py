from PIL import Image, ImageDraw
import copy
import math
import random
from color_models import RGB, HSV, LAB


"""
Collection of image generators based around applying color gradients to various shapes.
"""

"""
Every gradient can be created in either the RGB, HSV, or LAB color spaces.
To display a gradient in the desired mode, set the optional 'mode' parameter to the following, RGB by default:
-RGB - 'rgb' 
-HSV - 'hsv'
-LAB - 'lab'
"""


def random_colors(max_n=5):
    """
    Returns n random RGB colors, where k is a random value between 2 and n.
    :param max_n: max value of n
    :return: k random RGB colors
    """
    return RGB.n_random_rbg(random.randint(2, max_n))


def star(image, coordinates, cur_color):
    upper_left_x = coordinates[0]
    upper_left_y = coordinates[1]
    lower_right_x = coordinates[2]
    lower_right_y = coordinates[3]

    actual_vert = lower_right_y - upper_left_y
    actual_horz = lower_right_x - upper_left_x

    left_horz_dist = .35
    right_horz_dist = 1 - left_horz_dist
    upper_vert_dist = left_horz_dist
    lower_vert_dist = 1 - upper_vert_dist

    a = ((actual_horz / 2) + upper_left_x, upper_left_y)
    b = ((actual_horz * right_horz_dist) + upper_left_x, (actual_vert * upper_vert_dist) + upper_left_y)
    c = (lower_right_x, (actual_vert / 2) + upper_left_y)
    d = (b[0], (actual_vert * lower_vert_dist) + upper_left_y)
    e = (a[0], lower_right_y)
    f = ((actual_horz * left_horz_dist) + upper_left_x, d[1])
    g = (upper_left_x, c[1])
    h = (f[0], b[1])

    to_draw = ImageDraw.Draw(image)
    to_draw.polygon((a, b, c, d, e, f, g, h), fill=cur_color)


def rectangle(image, coordinates, cur_color):
    to_draw = ImageDraw.Draw(image)
    to_draw.rectangle(coordinates, fill=cur_color)


def ellipse(image, coordinates, cur_color):
    to_draw = ImageDraw.Draw(image)
    to_draw.ellipse(coordinates, fill=cur_color)


def arced_rectangle(image, coordinates, cur_color, x_perc, y_perc):
    def midpoint_curve_x(start_x, start_y, mid_x, mid_y, end_x, end_y):
        if not (start_x < mid_x < end_x):
            raise ValueError('Given x positions can\' interfere with each others sections!')

        coors = []
        pi = math.pi

        width_1 = round(abs(mid_x - start_x))
        for point in range(width_1):
            y = (mid_y - start_y) * math.sin((point * pi) / (width_1 * 2))
            coor = (point + start_x, y + start_y)
            coors.append(coor)

        width_2 = round(abs(end_x - mid_x))
        for point in range(width_2):
            y = (mid_y - end_y) * math.sin(((point + width_2) * pi) / (width_2 * 2))
            coor = (point + width_1 + start_x, y + end_y)
            coors.append(coor)

        return coors

    def midpoint_curve_y(start_x, start_y, mid_x, mid_y, end_x, end_y):
        if not (start_y < mid_y < end_y):
            raise ValueError('Given x positions can\' interfere with each others sections!')

        pi = math.pi
        coors = []

        width_1 = round(abs(mid_y - start_y))
        for point in range(width_1):
            x = (mid_x - start_x) * math.sin((point * pi) / (width_1 * 2))
            coor = (x + start_x, point + start_y)
            coors.append(coor)

        width_2 = round(abs(end_y - mid_y))
        for point in range(width_2):
            x = (mid_x - end_x) * math.sin(((point + width_2) * pi) / (width_2 * 2))
            coor = (x + end_x, point + width_1 + start_y)
            coors.append(coor)

        return coors

    upper_left_x = coordinates[0]
    upper_left_y = coordinates[1]
    lower_right_x = coordinates[2]
    lower_right_y = coordinates[3]

    actual_vert = lower_right_y - upper_left_y
    actual_horz = lower_right_x - upper_left_x

    horz_x_dist = x_perc * actual_horz
    horz_y_dist = y_perc * actual_vert

    vert_y_dist = x_perc * actual_vert
    vert_x_dist = y_perc * actual_horz

    top_x = lower_right_x - horz_x_dist
    top_y = upper_left_y + horz_y_dist

    right_x = lower_right_x - vert_x_dist
    right_y = lower_right_y - vert_y_dist

    bottom_x = upper_left_x + horz_x_dist
    bottom_y = lower_right_y - horz_y_dist

    left_x = upper_left_x + vert_x_dist
    left_y = upper_left_y + vert_y_dist

    top = midpoint_curve_x(upper_left_x, upper_left_y, top_x, top_y, lower_right_x, upper_left_y)
    right = midpoint_curve_y(lower_right_x, upper_left_y, right_x, right_y, lower_right_x, lower_right_y)
    bottom = midpoint_curve_x(upper_left_x, lower_right_y, bottom_x, bottom_y, lower_right_x, lower_right_y)
    left = midpoint_curve_y(upper_left_x, upper_left_y, left_x, left_y, upper_left_x, lower_right_y)

    right.reverse()
    top.reverse()
    coors = left + bottom + right + top

    to_draw = ImageDraw.Draw(image)
    to_draw.polygon(xy=coors, fill=cur_color)


def even_arced_rect(image, coordinates, cur_color):
    arced_rectangle(image, coordinates, cur_color, .5, .15)


def lopsided_arced_rect(image, coordinates, cur_color):
    arced_rectangle(image, coordinates, cur_color, .3, .2)


def diamond(image, coordinates, cur_color, vert, horz):
    upper_left_x = coordinates[0]
    upper_left_y = coordinates[1]
    lower_right_x = coordinates[2]
    lower_right_y = coordinates[3]

    actual_vert = lower_right_y - upper_left_y
    actual_horz = lower_right_x - upper_left_x
    horz_b = 1 - horz

    a = (upper_left_x, upper_left_y + (vert * (actual_vert)))
    b = ((horz_b * (actual_horz)) + upper_left_x, upper_left_y)
    c = ((horz * (actual_horz)) + upper_left_x, upper_left_y)
    d = (lower_right_x, upper_left_y + (vert * (actual_vert)))
    e = (((actual_horz) / 2) + upper_left_x, lower_right_y)

    coordinates = [a, b, c, d, e]
    to_draw = ImageDraw.Draw(image)
    to_draw.polygon(coordinates, fill=cur_color)


def even_diamond(image, coordinates, cur_color):
    even = .5
    return diamond(image, coordinates, cur_color, even, even)


def double_diamond(image, coordinates, cur_color):
    upper_left_x = coordinates[0]
    upper_left_y = coordinates[1]
    lower_right_x = coordinates[2]
    lower_right_y = coordinates[3]

    actual_vert = lower_right_y - upper_left_y
    actual_horz = lower_right_x - upper_left_x

    vert_a = .2
    vert_b = 1 - vert_a
    horz_a = .2
    horz_b = 1 - horz_a
    mid_offset = actual_horz * .35

    a = (upper_left_x, upper_left_y + (vert_a * (actual_vert)))
    b = ((horz_a * (actual_horz)) + upper_left_x, upper_left_y)
    c = ((horz_b * (actual_horz)) + upper_left_x, upper_left_y)
    d = (lower_right_x, upper_left_y + (vert_a * (actual_vert)))
    e = (((actual_horz) / 2) + upper_left_x + mid_offset, (actual_vert / 2) + upper_left_y)
    f = (lower_right_x, upper_left_y + (vert_b * (actual_vert)))
    g = ((horz_b * (actual_horz)) + upper_left_x, lower_right_y)
    h = ((horz_a * (actual_horz)) + upper_left_x, lower_right_y)
    i = (upper_left_x, upper_left_y + (vert_b * (actual_vert)))
    j = (((actual_horz) / 2) + upper_left_x - mid_offset, (actual_vert / 2) + upper_left_y)

    coordinates = [a, b, c, d, e, f, g, h, i, j]
    to_draw = ImageDraw.Draw(image)
    to_draw.polygon(coordinates, fill=cur_color)


def create_color_gradient(list_of_colors, n, mode='rgb', alpha=False, reflect=False):
    x = len(list_of_colors)

    if n <= x - 1:
        raise ValueError('')

    original_n = n
    if reflect:
        math.ceil(n / 2)

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
                if alpha:
                    gradient_values.append(b.output_as_rgba())
                else:
                    gradient_values.append(b.output())

    if reflect:
        gradient_values += gradient_values[::-1]

        if len(gradient_values) > original_n:
            gradient_values = gradient_values[:len(gradient_values) - 1]

    return gradient_values


def master_gradient(width, height, list_of_colors, shape, fill_background=True, mode='rgb', alpha=False):
    if width <= height:
        shorter_radius = math.ceil(width / 2)
        longer_radius = math.ceil(height / 2)
    else:
        shorter_radius = math.ceil(height / 2)
        longer_radius = math.ceil(width / 2)

    size = (width, height)
    gradient_values = create_color_gradient(list_of_colors, longer_radius, mode, alpha)
    ratio = shorter_radius / longer_radius

    if alpha:
        to_render = Image.new('RGBA', size)
    else:
        to_render = Image.new('RGB', size)

    if fill_background:
        to_render.paste(gradient_values[-1], [0, 0, to_render.size[0], to_render.size[1]])

    upper_left_x = 0
    upper_left_y = 0
    lower_right_x = to_render.width
    lower_right_y = to_render.height

    for i in range(longer_radius):
        coordinates = [upper_left_x, upper_left_y, lower_right_x, lower_right_y]
        cur_color = gradient_values[longer_radius - i - 1]
        shape(to_render, coordinates, cur_color)

        if width <= height:
            upper_left_y += 1
            upper_left_x = round(upper_left_y * ratio)
        else:
            upper_left_x += 1
            upper_left_y = round(upper_left_x * ratio)

        lower_right_x = to_render.width - upper_left_x
        lower_right_y = to_render.height - upper_left_y

    return to_render


def line_gradient(width, height, list_of_colors=random_colors(), mode='rgb', alpha=False):
    results = create_color_gradient(list_of_colors, width, mode, alpha)

    if alpha:
        to_render = Image.new('RGBA', (width, height))
    else:
        to_render = Image.new('RGB', (width, height))
    to_draw = ImageDraw.Draw(to_render)

    for idx, color in enumerate(results):
        to_draw.line([idx, 0, idx, height - 1], color, 0)

    return to_render


def lopsided_arced_rect_gradient(width, height, list_of_colors=random_colors(), fill_background=True, mode='rgb', alpha=False):
    return master_gradient(width, height, list_of_colors, lopsided_arced_rect, fill_background, mode, alpha)


def even_arced_rect_gradient(width, height, list_of_colors=random_colors(), fill_background=True, mode='rgb', alpha=False):
    return master_gradient(width, height, list_of_colors, even_arced_rect, fill_background, mode, alpha)


def star_gradient(width, height, list_of_colors=random_colors(), fill_background=True, mode='rgb', alpha=False):
    return master_gradient(width, height, list_of_colors, star, fill_background, mode, alpha)


def even_diamond_gradient(width, height, list_of_colors=random_colors(), fill_background=True, mode='rgb', alpha=False):
    return master_gradient(width, height, list_of_colors, even_diamond, fill_background, mode, alpha)


def diamond_gradient(width, height, list_of_colors=random_colors(), fill_background=True, mode='rgb', alpha=False):
    def diamond_jewel(image, coordinates, cur_color):
        return diamond(image, coordinates, cur_color, .25, .75)

    return master_gradient(width, height, list_of_colors, diamond_jewel, fill_background, mode, alpha)


def rectangle_gradient(width, height, list_of_colors=random_colors(), fill_background=True, mode='rgb', alpha=False):
    return master_gradient(width, height, list_of_colors, rectangle, fill_background, mode, alpha)


def ellipse_gradient(width, height, list_of_colors=random_colors(), fill_background=True, mode='rgb', alpha=False):
    return master_gradient(width, height, list_of_colors, ellipse, fill_background, mode, alpha)


def double_diamond_gradient(width, height, list_of_colors=random_colors(), fill_background=True, mode='rgb', alpha=False):
    return master_gradient(width, height, list_of_colors, double_diamond, fill_background, mode, alpha)
