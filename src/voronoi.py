from PIL import ImageDraw, Image
import random
from src.colormodels import RGB
import math


def euclidean_distance(x0, y0, x1, y1):
    return math.sqrt(((x1 - x0) ** 2) + ((y1 - y0) ** 2))


def manhattan_distance(x0, y0, x1, y1):
    return abs(y1 - y0) + abs(x1 - x0)

def ramanujans_ellipse_arc(x0, y0, x1, y1):
    a = abs(x1 - x0)
    b = abs(y1 - y0)
    pi = 3.14159
    return ((pi / 4) * ((3 * (a + b)) - math.sqrt(((3 * a) + b) * (a + (3 * b)))))

def random_feature_points(width, height, num_of_points):
    if num_of_points < 1:
        raise ValueError('Number of feature points must be >= 1')

    feature_points = list()
    for point in range(num_of_points):
        point_created = False

        while not point_created:  # Don't want duplicate feature points
            new_x = random.randint(0, width)
            new_y = random.randint(0, height)
            xy = (new_x, new_y)

            if xy not in feature_points:
                feature_points.append(xy)
                point_created = True

    return feature_points


def voronoi(width, height, feature_points, distance):
    feature_points_and_coors = {}
    for feature_point in feature_points:
        feature_points_and_coors[feature_point] = []

    for row in range(height):
        for column in range(width):
            cur_point = (column, row)

            dists_from_features = {}
            for feature_point in feature_points_and_coors:
                cur_dist = distance(cur_point[0], cur_point[1], feature_point[0], feature_point[1])
                dists_from_features[cur_dist] = feature_point

            min_dist = min(dists_from_features)
            min_feature_point= dists_from_features[min_dist]
            feature_points_and_coors[min_feature_point].append(cur_point)

    return list(feature_points_and_coors.values())


def lloyds_algorithm(width, height, num_of_points, distance):
    old_feature_points = random_feature_points(width, height, num_of_points)
    new_feature_points = old_feature_points

    avg_dist_moved = 2
    while avg_dist_moved > .5:
        result_groups = voronoi(width, height, new_feature_points, distance)
        
        old_feature_points = new_feature_points
        new_feature_points = []
        avg_dist_moved = 0
        for idx, group in enumerate(result_groups):
            cum_x = 0
            cum_y = 0
            n = 0
            for coor in group:
                cum_x += coor[0]
                cum_y += coor[1]
                n += 1

            cum_x /= n
            cum_y /= n
            xy = (cum_x, cum_y)

            old_feature_points_coor = old_feature_points[idx]
            avg_dist_moved += euclidean_distance(xy[0], xy[1], old_feature_points_coor[0], old_feature_points_coor[1])
            new_feature_points.append(xy)
            print(avg_dist_moved)

        avg_dist_moved /= len(new_feature_points)

    return result_groups


def render_voronoi(groupings):
    max_width = 0
    max_height = 0
    for group in groupings:
        for coor in group:
            x = coor[0]
            y = coor[1]
            if x > max_width:
                max_width = x

            if y > max_height:
                max_height = y

    to_render = Image.new('RGB', (max_width, max_height))
    to_draw = ImageDraw.Draw(to_render)

    for idx, group in enumerate(groupings):
        cur_color = RGB.random_rgb().output()
        for coor in group:
            to_draw.point(coor, fill=cur_color)

    return to_render

if __name__ == '__main__' :
    x = 500
    results = lloyds_algorithm(x, x, 20, manhattan_distance)
    render_voronoi(results).show()
