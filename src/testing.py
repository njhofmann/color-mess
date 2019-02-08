from PIL import ImageDraw, Image
import math
from colormodels import RGB, HSV
from gradients import star_gradient, even_arced_rect_gradient, lopsided_arced_rect_gradient, create_color_gradient
import random
from schemas import n_evenly_spaced_colors
from backgrounds import regular_shape, plaid, granite, straight_granite, gradient_shifts
from voronoi import VoronoiDiagram, euclidean_distance, ellipse_arc_distance, manhattan_distance
import os


def colored_voronoi_diagram(x, y, num_of_points=random.randint(5,20)):
    colors = n_evenly_spaced_colors(RGB.random_rgb(), num_of_points)
    diagram = VoronoiDiagram(x, y, num_of_points, ellipse_arc_distance)
    diagram.optimize()

    img = Image.new('RGB', (x, y))
    draw = ImageDraw.Draw(img)

    for idx in range(num_of_points):
        cur_color = colors[idx]
        cur_set = diagram.coor_groupings[idx]
        for point in cur_set:
            draw.point(point, cur_color.output())

    return img


def multi_circles(width, length, num_of_points=random.randint(3,7), num_of_colors=random.randint(4,10), optimize=False):
    vrn = VoronoiDiagram(width, length, num_of_points, euclidean_distance)
    if optimize:
        vrn.optimize()
    points = vrn.feature_points

    points_to_corners = []
    corners = [(0, 0), (width, length), (width, 0), (0, length)]
    for point in points:
        corner_dists = []
        for corner in corners:
            cur_dist = euclidean_distance(point[0], point[1], corner[0], corner[1])
            corner_dists.append(cur_dist)
        points_to_corners.append(max(corner_dists))
    max_dist = math.ceil(min(points_to_corners))

    colors = n_evenly_spaced_colors(RGB.random_rgb(), num_of_colors)
    gradient = create_color_gradient(colors, max_dist)

    img = Image.new('RGB', (width, length))
    draw = ImageDraw.Draw(img)
    for idx in range(max_dist - 1, -1, -1):
        cur_color = gradient[idx]
        for point in points:
            x = point[0]
            y = point[1]
            coors = (x - idx, y - idx, x + idx, y + idx)
            draw.ellipse(coors, cur_color)

    return img


if __name__ == '__main__':
    img = multi_circles(1080, 1920, num_of_points=10)
    img.show()
    img.save("testing.bmp", 'BMP')


