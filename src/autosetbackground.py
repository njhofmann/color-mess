from backgrounds import gradient_shifts, granite, regular_shape, straight_granite, plaid, rotated_diamond
from gradients import star_gradient, rectangle_gradient, even_diamond_gradient, diamond_gradient, \
    double_diamond_gradient, ellipse_gradient, line_gradient
import sys
import random
import os
import ctypes
from PIL import Image


def create_and_set_backgound():
    width = 1920
    height = 1080
    shape = random.choice((granite, gradient_shifts, regular_shape, straight_granite, plaid, rotated_diamond,
                            star_gradient, rectangle_gradient, even_diamond_gradient, double_diamond_gradient,
                            ellipse_gradient, diamond_gradient, line_gradient))

    img = shape(width, height)

    if img.mode == 'HSV': # Color mode must be RGB as not every file type supports HSV or other color spaces
        img = img.convert('RGB')

    filepath ='C:\\Users\\inate\\PycharmProjects\\color-mess\\resources\\wallpaper.bmp' # File path from program root
    img.save(filepath, 'BMP')
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filepath, 3)


if __name__ == '__main__':
    create_and_set_backgound()