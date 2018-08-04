from src import *
from PIL import ImageDraw, Image

a = RGB.random_rgb()
b = RGB.random_rgb()
c = RGB.random_rgb()
colors = [a, b, c]
img = diamond_gradient(colors, 1000, 1000)
img.show()