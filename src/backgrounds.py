from colormodels import RGB, HSV
from gradients import Gradients
from PIL import Image, ImageDraw
import collections
import random


shapes = (Gradients.diamond_gradient, Gradients.double_diamond_gradient, Gradients.star_gradient,
          Gradients.even_diamond_gradient, Gradients.ellipse_gradient, Gradients.rectangle_gradient)


def gradient_shifts(width, height, sections):
    if sections > width:
        raise ValueError("Can't have more sections than the given width!")
    elif width % sections != 0:
        raise ValueError('Given number of sections must be equally divisible by the given width!')

    rgbs = RGB.n_random_rbgs(3)
    gradient = collections.deque(Gradients.create_color_gradient(rgbs, height, 'rgb', False, True))
    shifts = [random.choice((True, False)) for i in range(sections)] # Shift up by 1 if True, down by 1 if False

    to_render = Image.new('RGB', (width, height))
    to_draw = ImageDraw.Draw(to_render)

    section_size = round(width / sections)
    cur_column = 0
    n = round(width * .025)
    for shift in shifts:
        if shift:
            gradient.rotate(-n)
        else:
            gradient.rotate(n)

        for column in range(section_size):
            for row in range(height):
                to_draw.point((cur_column, row), gradient[row])
            cur_column += 1

    return to_render



def straight_granite(width, height):
    min_value = 0
    max_value = 100
    hsv = HSV.random_hsv()

    temp_height = height + 1
    to_render = Image.new('HSV', (width, temp_height))
    to_draw = ImageDraw.Draw(to_render)

    def mutation_value():
        ending = 10
        return random.randint(-ending, ending)

    def check_new_value(value):
        if value < min_value:
            return min_value
        elif value > max_value:
            return max_value
        return value

    for pixel in range(0, width):
        hsv.value = random.randint(min_value, max_value)
        to_draw.point((pixel, 0), fill=hsv.output())

    for row in range(1, temp_height):
        for column in range(0, width):
            edge_value = 50

            if column == 0:
                top_left_value = edge_value
            else:
                top_left_value = to_render.getpixel((column - 1, row - 1))[2]

            top_value = to_render.getpixel((column, row - 1))[2]

            if column == (width - 1):
                top_right_value = edge_value
            else:
                top_right_value = to_render.getpixel((column + 1, row - 1))[2]

            new_value = (top_left_value + top_value + top_right_value) / 3
            new_value += mutation_value()
            new_value = check_new_value(new_value)
            hsv.value = new_value
            to_draw.point((column, row), fill=hsv.output())

    to_render = to_render.crop((0, 1, width, temp_height))
    return to_render


def granite(width, height):
    min_value = 0
    max_value = 100
    hsv = HSV.random_hsv()

    to_render = Image.new('HSV', (width, height))
    to_draw = ImageDraw.Draw(to_render)

    def mutation_value():
        ending = 10
        return random.randint(-ending, ending)

    def check_new_value(value):
        if value < min_value:
            return min_value
        elif value > max_value:
            return max_value
        return value

    # Set value for starting pixel in upper left corner
    corner_start_value = random.randint(min_value, max_value)
    hsv.value = corner_start_value
    to_draw.point((0, 0), fill=hsv.output())

    for pixel in range(1, width):
        new_value = hsv.value + mutation_value()
        new_value = check_new_value(new_value)
        hsv.value = new_value
        to_draw.point((pixel, 0), fill=hsv.output())

    hsv.value = to_render.getpixel((0, 0))[2]
    for pixel in range(1, height):
        new_value = hsv.value + mutation_value()
        new_value = check_new_value(new_value)
        hsv.value = new_value
        to_draw.point((0, pixel), fill=hsv.output())

    for row in range(1, height):
        for column in range(1, width):
            left_value = to_render.getpixel((column - 1, row))[2]
            bottom_value = to_render.getpixel((column, row - 1))[2]
            avg_value = round((left_value + bottom_value) / 2)
            new_value = avg_value + mutation_value()
            new_value = check_new_value(new_value)
            hsv.value = new_value
            to_draw.point((column, row), fill=hsv.output())

    return to_render


def regular_shape(width, height):
    n = random.randint(2, 6)
    colors = RGB.n_random_rgba(n)
    shape_to_render = random.choice(shapes)
    gradient = shape_to_render(colors, width, height, True, 'rgb', True)
    return gradient


def plaid(width, height):
    n = random.randint(2, 6)
    colors = RGB.n_random_rgba(n)
    longer_length = max(width, height)

    grad = Gradients.line_gradient(colors, longer_length, longer_length, 'rgb', True)
    rotated_grad = grad.rotate(90)
    result = Image.blend(grad, rotated_grad, .5)

    dist_between = (width - height) / 2
    if longer_length == width:
        return result.crop((0, dist_between, width, width - dist_between))
    else:
        return result.crop((dist_between, 0, height - dist_between, height))


def rotated_diamond(width, height):
    n = random.randint(2, 8)
    colors = RGB.n_random_rgba(n)
    gradient = Gradients.diamond_gradient(colors, width, height, True, 'rgb', True)
    rotated_gradient = gradient.rotate(180)
    vert = Image.alpha_composite(gradient, rotated_gradient)
    horz = vert.rotate(90)
    result = Image.alpha_composite(vert, horz)
    return result


