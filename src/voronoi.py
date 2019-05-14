from PIL import ImageDraw, Image
import random
from src.colormodels import RGB
import math
import sys


def radivojac_distance(x0, y0, x1, y1):
    unnormalized = euclidean_distance(x0, y0, x1, y1)
    x_value = max(x0, x1, abs(x0 - x1))
    y_value = max(y0, y1, abs(y0 - y1))
    return unnormalized / (x_value + y_value)


def euclidean_distance(x0, y0, x1, y1):
    """
    Regular Euclidean distance algorithm.
    :param x0: x value of the first coordinate
    :param y0: y value of the first coordinate
    :param x1: x value of the second coordinate
    :param y1: y value of the second coordinate
    :return: euclidean distance
    """
    return math.sqrt(((x1 - x0) ** 2) + ((y1 - y0) ** 2))


def manhattan_distance(x0, y0, x1, y1):
    """
    Manhattan distance algorithm
    :param x0: x value of the first coordinate
    :param y0: y value of the first coordinate
    :param x1: x value of the second coordinate
    :param y1: y value of the second coordinate
    :return: manhattan distance
    """
    return abs(y1 - y0) + abs(x1 - x0)


def ellipse_arc_distance(x0, y0, x1, y1):
    """
    Distance algorithm based on Ramanujan's approximation for an ellipse's circumference.
    :param x0: x value of the first coordinate
    :param y0: y value of the first coordinate
    :param x1: x value of the second coordinate
    :param y1: y value of the second coordinate
    :return: approximated ellipse arc distance
    """
    a = abs(x1 - x0)
    b = abs(y1 - y0)
    pi = 3.14159
    return (pi / 4) * ((3 * (a + b)) - math.sqrt(((3 * a) + b) * (a + (3 * b))))


class VoronoiDiagram:
    """
    Represents the feature points, coordinate groupings, height, and width of a Voronoi diagram.
    """

    def __init__(self, width, height, number_of_feature_points, optimization_threshold=1, distance=euclidean_distance):
        """
        Creates a Voronoi diagram from a given width, height, number of feature points, and distance algorithm.
        :param width: max width of this Voronoi diagram
        :param height: max height of this Voronoi diagram
        :param number_of_feature_points: number of feature points this Voronoi diagram will always have
        :param optimization_threshold: stopping threshold to dictate when to stop optimization, lower value = closer clusters
        :param distance: distance algorithm to use for computing the distance between points and feature points
        """
        self.width = width
        self.height = height
        self.distance = distance
        self.optimization_threshold = optimization_threshold

        if number_of_feature_points < 1:
            raise ValueError('Number of feature points must be >= 1')

        self.feature_points = set()
        for point in range(number_of_feature_points):
            point_created = False

            while not point_created:  # Don't want duplicate feature points
                new_x = random.randint(0, width)
                new_y = random.randint(0, height)
                xy = (new_x, new_y)

                if xy not in self.feature_points:
                    self.feature_points.add(xy)
                    point_created = True

        self.coor_groupings = []
        self.find_groupings()

    def find_groupings(self):
        """
        Finds the latest coordinate groupings for this Voronoi diagram given its current set of feature points.
        :return: None
        """

        feature_points_and_coor_groupings = dict.fromkeys(self.feature_points, list())

        for row in range(self.height):
            for column in range(self.width):
                cur_point = (column, row)
                cur_closest_feature_point = self.feature_points[0]
                cur_closest_feature_point_dist = sys.maxsize

                for feature_point in feature_points_and_coor_groupings.keys():
                    cur_dist = self.distance(cur_point[0], cur_point[1], feature_point[0], feature_point[1])
                    if cur_dist < cur_closest_feature_point_dist:
                        cur_closest_feature_point_dist = cur_dist
                        cur_closest_feature_point = feature_point

                feature_points_and_coor_groupings.get(cur_closest_feature_point).append(cur_point)

        self.coor_groupings = list(feature_points_and_coor_groupings.values())

    def optimize(self):
        """
        'Optimizes' this Voronoi diagram according to k-means clustering / Lloyd's algorithm to produce largely
        similarly sized groupings and evenly spaced feature points.
        :return: None
        """
        old_feature_points = self.feature_points
        new_feature_points = old_feature_points

        avg_dist_moved = None
        while avg_dist_moved is None or avg_dist_moved > self.optimization_threshold:  # Adjust me! 10 for ellipse arc, 1.9 otherwise
            print(avg_dist_moved)
            self.find_groupings()

            old_feature_points = new_feature_points
            new_feature_points = []

            avg_dist_moved = 0
            for idx, group in enumerate(self.coor_groupings):
                group_length = len(group)
                if group_length > 0:
                    cum_x = 0
                    cum_y = 0

                    for coor in group:
                        cum_x += coor[0]
                        cum_y += coor[1]

                    cum_x /= group_length
                    cum_y /= group_length

                    xy = (cum_x, cum_y)

                    old_feature_points_coor = old_feature_points[idx]
                    avg_dist_moved += euclidean_distance(xy[0], xy[1], old_feature_points_coor[0],
                                                         old_feature_points_coor[1])
                    new_feature_points.append(xy)

            avg_dist_moved /= len(new_feature_points)
            self.feature_points = new_feature_points

    def view(self, display_feature_points=True):
        """
        Displays the feature points and group of this Voronoi diagram on an image.
        :return:
        """
        to_render = Image.new('RGB', (self.width, self.height))
        to_draw = ImageDraw.Draw(to_render)

        for idx, group in enumerate(self.coor_groupings):
            cur_color = RGB.random_rgb().output()
            for coor in group:
                to_draw.point(coor, fill=cur_color)

        if display_feature_points:
            for coor in self.feature_points:
                to_draw.point(coor, (0, 0, 0))

        to_render.show()


if __name__ == '__main__':
    x = 200
    diagram = VoronoiDiagram(x, x, 20, distance=radivojac_distance, optimization_threshold=2)
    diagram.optimize()
    diagram.view()