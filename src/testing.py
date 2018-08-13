from src import *
from PIL import Image, ImageDraw
import math
from src.gradients import Gradients
from src.backgrounds import regular_shape, plaid, granite, straight_granite


def distance(x0, y0, x1, y1):
    return math.sqrt(((x1 - x0) ** 2) + ((y1 - y0) ** 2))

print(distance(0, 0, 10, 12))

