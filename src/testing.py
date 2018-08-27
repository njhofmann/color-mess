from PIL import Image, ImageDraw
import math
from gradients import Gradients
from backgrounds import regular_shape, plaid, granite, straight_granite, gradient_shifts


img = gradient_shifts(1920, 1080, 20)
img.save('/Users/inate/Pictures/foo.bmp', 'BMP')
