from src import *
from PIL import ImageDraw, Image

a = RGB.n_random_rgba(6)
for i in a:
    print(i.output_as_rgba())
a = diamond_gradient(a, 1500, 2000, False, 'lab', True)
rot = a.rotate(180)
result = Image.alpha_composite(a, rot)
rot = result.rotate(90)
result = Image.alpha_composite(rot, result)
print(result.mode)
result.crop([250, 250, 1250, 1750]).show()