from src import *
from PIL import Image
import random

def colors_to_use():
    schemas = []


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