from PIL import ImageDraw, Image
import math
from colormodels import RGB, HSV
from gradients import star_gradient, even_arced_rect_gradient, lopsided_arced_rect_gradient
import random
from backgrounds import regular_shape, plaid, granite, straight_granite, gradient_shifts
from voronoi import VoronoiDiagram, euclidean_distance

side = 500
vor = VoronoiDiagram(side, side, 3)
vor.optimize()
main_points = tuple(vor.feature_points)

main_point_color = HSV.random_hsv()
main_points_to_colors = dict()
main_points = []
for i in vor.feature_points:
    to_add = (round(i[0]), round(i[1]))
    main_points.append(to_add)
    main_points_to_colors[to_add] = HSV(main_point_color.hue, random.randint(50, 100), 80)
main_points = tuple(main_points)

img = Image.new('HSV', (side, side))
draw = ImageDraw.Draw(img)

for row in range(side):
    for col in range(side):
        cur_points = (row, col)

        cur_main_point_dists = {}
        cum_dist = 0
        for pt in main_points:
            cur_dist = euclidean_distance(cur_points[0], cur_points[1], pt[0], pt[1])
            cur_main_point_dists[pt] = cur_dist
            cum_dist += cur_dist

        sum_dist = 0
        for pt in main_points:
            cur_dist = cur_main_point_dists[pt]
            new_dist = cum_dist - cur_dist
            cur_main_point_dists[pt] = new_dist
            sum_dist += new_dist

        cum_sat = 0
        for pt in main_points:
            cur_dist = cur_main_point_dists.get(pt)
            weight = cur_dist / sum_dist
            cur_color = main_points_to_colors.get(pt)
            cum_sat += weight * cur_color.saturation

        cur_color = (main_point_color.hue, round(cum_sat / len(main_points)), main_point_color.value)
        print(cur_color)
        draw.point(cur_points, cur_color)

img.show()





