from PIL import ImageDraw, Image
import math
from colormodels import RGB, HSV
from gradients import star_gradient, even_arced_rect_gradient, lopsided_arced_rect_gradient, create_color_gradient
import random
from schemas import n_evenly_spaced_colors
from backgrounds import regular_shape, plaid, granite, straight_granite, gradient_shifts
from voronoi import VoronoiDiagram, euclidean_distance, ellipse_arc_distance, manhattan_distance
import os


flowers = Image.open('toucan.jpg')
width, height = flowers.size
dummy_img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(dummy_img)
num_of_points = round((width * height) / 100)
vor = VoronoiDiagram(width, height, num_of_points)
vor.optimize()

for group in vor.coor_groupings:
    num_of_coors = len(group)
    avg_red, avg_green, avg_blue = 0, 0, 0
    for coor in group:
        red, green, blue = flowers.getpixel(coor)
        avg_red += red
        avg_green += green
        avg_blue += blue

    avg_red /= num_of_coors
    avg_green /= num_of_coors
    avg_blue /= num_of_coors
    new_color = (round(avg_red), round(avg_green), round(avg_blue))

    for coor in group:
        draw.point(coor, new_color)

dummy_img.save('glass.bmp', 'BMP')



