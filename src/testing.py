from PIL import ImageDraw, Image
import math
from colormodels import RGB, HSV
from gradients import star_gradient, even_arced_rect_gradient, lopsided_arced_rect_gradient
import random
from schemas import n_evenly_spaced_colors
from backgrounds import regular_shape, plaid, granite, straight_granite, gradient_shifts
from voronoi import VoronoiDiagram, euclidean_distance, ellipse_arc_distance, manhattan_distance
import os

print(os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources\wallpaper.bmp')))



