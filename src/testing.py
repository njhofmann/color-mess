from PIL import Image, ImageDraw
import math
from src.gradients import Gradients
from src.backgrounds import regular_shape, plaid, granite, straight_granite


img = regular_shape(500, 500)
img.show()
img.save('C:/Users/inate/Pictures/Lloyd/foo.bmp')
