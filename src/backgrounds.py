from src import *
from PIL import Image, ImageDraw
import random

def colors_to_use():
    schemas = []

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

    real_height = height - 1
    real_width = width - 1

    for pixel in range(1, real_width):
        new_value = hsv.value + mutation_value()
        new_value = check_new_value(new_value)
        hsv.value = new_value
        to_draw.point((pixel, 0), fill=hsv.output())

    hsv.value = to_render.getpixel((0, 0))[2]
    for pixel in range(1, real_height):
        new_value = hsv.value + mutation_value()
        new_value = check_new_value(new_value)
        hsv.value = new_value
        to_draw.point((0, pixel), fill=hsv.output())

    for row in range(1, real_width):
        for column in range(1, real_height):
            left_value = to_render.getpixel((column - 1, row))[2]
            bottom_value = to_render.getpixel((column, row - 1))[2]
            avg_value = round((left_value + bottom_value) / 2)
            new_value = avg_value + mutation_value()
            new_value = check_new_value(new_value)
            hsv.value = new_value
            to_draw.point((column, row), fill=hsv.output())

    to_rotate = random.randint(1, 3)
    for i in range(to_rotate):
        to_render = to_render.rotate(90)

    return to_render



def regular_shape(width, height):
    n = random.randint(2, 8)
    colors = RGB.n_random_rgba(n)
    shapes = [double_diamond_gradient]
    shape_to_render = random.choice(shapes)
    gradient = shape_to_render(colors, width, height, True, 'rgb', True)
    return gradient

def plaid(width, height):
    n = random.randint(2, 8)
    colors = RGB.n_random_rgba(n)
    grad = line_gradient(colors, width, height, 'rgb')
    rotated_grad = grad.rotate(90)
    result = Image.blend(grad, rotated_grad, .5)
    return result


def rotated_diamond(width, height):
    n = random.randint(2, 8)
    colors = RGB.n_random_rgba(n)
    gradient = diamond_gradient(colors, width, height, True, 'rgb', True)
    rotated_gradient = gradient.rotate(180)
    vert = Image.alpha_composite(gradient, rotated_gradient)
    horz = vert.rotate(90)
    result = Image.alpha_composite(vert, horz)
    return result


def rotated_even_diamond(width, height):
    n = random.randint(2, 8)
    colors = RGB.n_random_rgba(n)
    gradient = even_diamond_gradient(colors, width, height, True, 'rgb', True)
    rotated_gradient = gradient.rotate(45)
    vert = Image.blend(gradient, rotated_gradient, .5)
    horz = vert.rotate(180)
    result = Image.blend(vert, horz, .5)
    return result


regular_shape(3000, 2000).show()