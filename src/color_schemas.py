from PIL import Image, ImageDraw
from color_models import RGB, HSV
import random

"""
Collection of methods for generating appealing color schemas.
"""


def random_number_of_colors():
    """
    Returns a random number of colors to produce from a preselected range.
    :return:
    """
    return random.randint(3, 8)


def random_range():
    """
    Returns a random number from a preselected range to use as a range for value, hue, or saturation.
    :return:
    """
    return random.randint(30, 70)


def n_colors_over_saturation_range(starting_color=RGB.random_rgb(), n=random_number_of_colors(), saturation=random_range()):
    """
    Returns n colors with same hue and value differing over a given saturation range.
    :param starting_color: color to start from
    :param n: number of colors to produce
    :param saturation: range of saturation to make colors from
    :return: list of colors over saturation range
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    elif saturation > 100:
        raise ValueError('Saturation range can\'t be > 100!')

    starting_color = starting_color.to_hsv()

    increment = saturation / (n - 1)
    cur_sat = (HSV.max_sv / 2) - (saturation / 2)
    results = []
    for idx in range(n):
        to_add = HSV(starting_color.hue, starting_color.saturation, cur_sat)
        results.append(to_add.to_rgb())
        cur_sat += increment

    return results


def n_colors_over_value_range(starting_color=RGB.random_rgb(), n=random_number_of_colors(), value=random_range()):
    """
    Returns n colors with same hue and saturation differing over a given value range.
    :param starting_color: color to start from
    :param n: number of colors to produce
    :param value: range of value to make colors from
    :return: list of colors of value range
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    elif value > 100:
        raise ValueError('Saturation range can\'t be > 100!')

    starting_color = starting_color.to_hsv()

    increment = value / (n - 1)
    cur_value = (HSV.max_sv / 2) - (value / 2)
    results = []
    for idx in range(n):
        to_add = HSV(starting_color.hue, starting_color.saturation, cur_value)
        results.append(to_add.to_rgb())
        cur_value += increment

    return results


def n_similar_colors(starting_color=RGB.random_rgb(), n=random_number_of_colors(), x=random_range()):
    """
    Returns a list of n colors 'similar' to each other, or n colors even spaced out over the hue scale in the HSV
    color space, starting from a given RGB color.
    :param starting_color: color to start from
    :param n: number of colors to produce
    :param x: range of hue to make colors from
    :return: list of n similar colors
    """
    starting_color = starting_color.to_hsv()
    hue = starting_color.hue
    start = (hue - x) % 360

    n -= 1
    if n < 2:
        increment = x * 2
    else:
        increment = (x * 2) / (n + 1)

    cur_hue = start
    results = []
    for idx in range(n + 1):
        to_add = HSV(cur_hue, starting_color.saturation, starting_color.value).to_rgb()
        results.append(to_add)
        cur_hue = (cur_hue + increment) % 360

    return results


def n_evenly_spaced_colors(starting_color=RGB.random_rgb(), n=random_number_of_colors()):
    """
    Returns a list of n colors evenly spaced out across the hue scale in the HSV color space from a given RGB color.
    :param starting_color: color to start from
    :param n: number of colors to include
    :return:
    """
    results = [starting_color]
    starting_color = starting_color.to_hsv()
    increment = 360 / n
    n -= 1
    cur_hue = starting_color.hue

    for new_color in range(n):
        cur_hue = (cur_hue + increment) % 360
        to_add = HSV(cur_hue, starting_color.saturation, starting_color.value)
        results.append(to_add.to_rgb())

    return results


def view_schema(colors):
    """
    Helper method for viewing schemas
    :param colors: list of colors to view
    :return: None
    """
    var = 100
    img = Image.new('RGB', (len(colors) * var, var))
    draw = ImageDraw.Draw(img)

    for idx, color in enumerate(colors):
        draw.rectangle([idx * var, 0, (idx + 1) * var, var], fill=color.output())

    img.show()


if __name__ == '__main__':
    view_schema(n_colors_over_saturation_range())
