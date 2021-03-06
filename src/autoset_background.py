from misc_generators import gradient_shifts, granite, regular_shape, straight_granite, plaid, rotated_diamond
from gradients import star_gradient, rectangle_gradient, even_diamond_gradient, diamond_gradient, \
    double_diamond_gradient, ellipse_gradient, line_gradient, lopsided_arced_rect_gradient, even_arced_rect_gradient
from color_schemas import n_evenly_spaced_colors, n_similar_colors, n_colors_over_saturation_range, n_colors_over_value_range
from color_models import RGB
import random
import ctypes
import os


def create_and_set_background():
    """
    Selects and runs a random image generation algorithm, then sets outputted image to the computer's background.
    :return: None
    """
    width = 1920
    height = 1080
    shape = random.choice((gradient_shifts, regular_shape, plaid, rotated_diamond,
                            star_gradient, rectangle_gradient, even_diamond_gradient, double_diamond_gradient,
                            ellipse_gradient, diamond_gradient, line_gradient, even_arced_rect_gradient,
                           lopsided_arced_rect_gradient))

    color_options = random.choice((n_evenly_spaced_colors, n_similar_colors, RGB.n_random_rbg,
                                   n_colors_over_saturation_range, n_colors_over_value_range))
    colors = color_options()

    img = shape(width, height, colors)

    # Color mode must be RGB as not every file type supports HSV or other color spaces
    if img.mode == 'HSV':
        img = img.convert('RGB')

    rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = os.path.join(rootpath, 'resources\\my_wallpaper.bmp')
    img.save(filename, 'BMP')
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filename, 3)


if __name__ == '__main__':
    create_and_set_background()