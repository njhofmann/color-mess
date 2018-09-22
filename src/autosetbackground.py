from backgrounds import gradient_shifts, granite, regular_shape, straight_granite, plaid, rotated_diamond
from gradients import star_gradient, rectangle_gradient, even_diamond_gradient, diamond_gradient, \
    double_diamond_gradient, ellipse_gradient, line_gradient, lopsided_arced_rect_gradient, even_arced_rect_gradient
from schemas import n_evenly_spaced_colors, n_similar_colors
from colormodels import RGB
import random
import ctypes


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

    color_options = random.choice((n_evenly_spaced_colors, n_similar_colors, RGB.n_random_rbg))
    colors = color_options()

    img = shape(width, height, colors)

    if img.mode == 'HSV': # Color mode must be RGB as not every file type supports HSV or other color spaces
        img = img.convert('RGB')

    filename = 'C:\\Users\\inate\\PycharmProjects\\color-mess\\resources\\wallpaper.bmp'  # File path from program root
    img.save(filename, 'BMP')
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filename, 3)


if __name__ == '__main__':
    create_and_set_background()