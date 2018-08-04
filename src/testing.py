from src import *
from PIL import ImageDraw, Image

colors = RGB.x_random_rbgs(7)
img = diamond_gradient(colors, 2000, 2500, True)
back = img.rotate(90)
result = Image.blend(img, back, .5)
rotate = result.rotate(180)
result = Image.blend(result, rotate, .5)
rotate = result.rotate(45)
result = Image.blend(result, rotate, .5)
result.show()