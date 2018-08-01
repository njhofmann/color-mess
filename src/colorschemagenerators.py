from PIL import Image, ImageDraw
from src.colormodels import RGB, HSV


def n_colors_over_value_range(starting_color, n, value):
    starting_color = starting_color.to_hsv()

    increment = value / (n - 1)
    cur_value = starting_color.value
    results = []
    for idx in range(n):
        to_add = HSV(starting_color.hue, starting_color.saturation, cur_value)
        results.append(to_add.to_rgb())
        cur_value = (cur_value + increment) % 100

    return results


def n_analogous_colors_over_x(starting_color, n, x):
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


def n_evenly_spaced_colors(starting_color, n):
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


def view_schema(clrs):
    var = 100
    img = Image.new('RGB', (len(clrs) * var, var))
    draw = ImageDraw.Draw(img)

    for idx, color in enumerate(clrs):
        draw.rectangle([idx * var, 0, (idx + 1) * var, var], fill=color.output_rgb())

    img.show()
