from PIL import ImageDraw, Image
import math
from colormodels import RGB
from gradients import star_gradient, even_arced_rect_gradient, lopsided_arced_rect_gradient
import math
from backgrounds import regular_shape, plaid, granite, straight_granite, gradient_shifts
from voronoi import VoronoiDiagram, euclidean_distance

side = 500
vor = VoronoiDiagram(side, side, 3)
vor.optimize()
main_points = tuple(vor.feature_points)

main_points_to_colors = dict()
main_points = []
for i in vor.feature_points:
    to_add = (round(i[0]), round(i[1]))
    main_points.append(to_add)
    main_points_to_colors[to_add] = RGB.random_rgb()
main_points = tuple(main_points)


img = Image.new('RGB', (side, side))
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

        cum_red = 0
        cum_green = 0
        cum_blue = 0
        for pt in main_points:
            cur_dist = cur_main_point_dists.get(pt)
            weight = cur_dist / sum_dist
            cur_color = main_points_to_colors.get(pt)
            cum_red += weight * cur_color.red
            cum_green += weight * cur_color.green
            cum_blue += weight * cur_color.blue

        l = len(main_points)
        cum_red /= l
        cum_green /= l
        cum_blue /= l
        cum_red = round(cum_red)
        cum_green = round(cum_green)
        cum_blue = round(cum_blue)

        color = RGB(cum_red, cum_green, cum_blue)
        color = color.to_hsv()
        color.value = 80
        color.to_rgb()

        draw.point(cur_points, color.output())

img.show()





