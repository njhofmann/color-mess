from backgrounds import gradient_shifts
import sys
import random
import os
import ctypes


def create_and_set_backgound():
    width = 1920
    height = 1080
    possible_sections = random.choice((4, 6, 8, 16, 20, 40, 60))
    img = gradient_shifts(width, height, possible_sections)

    filepath ='C:\\Users\\inate\\PycharmProjects\\color-mess\\resources\\wallpaper.bmp' # File path from program root
    img.save(filepath, 'BMP')
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filepath, 3)


if __name__ == '__main__':
    print(os.path.dirname(os.getcwd()) + '\\resources\\wallpaper.bmp')
    create_and_set_backgound()