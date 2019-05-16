from voronoi import  VoronoiDiagram, euclidean_distance
from colormodels import RGB
import math
import random
from PIL import Image, ImageDraw
from gradients import create_color_gradient


def multi_circles(width, length, num_of_points=random.randint(3,7), num_of_colors=random.randint(4,10), optimize=False):
    vrn = VoronoiDiagram(width, length, num_of_points, optimization_threshold=5)
    if optimize:
        vrn.optimize()
    points = vrn.feature_points

    points_to_corners = []
    corners = [(0, 0), (width, length), (width, 0), (0, length)]
    for corner in corners:
        min_dist = None
        for point in points:
            cur_dist = euclidean_distance(point[0], point[1], corner[0], corner[1])
            if min_dist is None:
                min_dist = cur_dist
            elif cur_dist < min_dist:
                min_dist = cur_dist
        points_to_corners.append(min_dist)
    max_dist = math.ceil(max(points_to_corners))

    colors = RGB.n_random_rbg(num_of_colors)
    gradient = create_color_gradient(colors, max_dist)

    img = Image.new('RGB', (width, length), gradient[-1])
    draw = ImageDraw.Draw(img)
    for idx in range(max_dist - 1, -1, -1):
        cur_color = gradient[idx]
        for point in points:
            x = point[0]
            y = point[1]
            coors = (x - idx, y - idx, x + idx, y + idx)
            draw.ellipse(coors, cur_color)

    return img


def frosted_glass(img_path, reduced_height=500):
    image = Image.open(img_path)
    width, height = image.size

    resize_height = reduced_height
    resize_width = round(resize_height * (width / height))
    image = image.resize((resize_width, resize_height))

    dummy_img = Image.new('RGB', (resize_width, resize_height))
    draw = ImageDraw.Draw(dummy_img)
    num_of_points = round((resize_width * resize_width) / 100)
    vor = VoronoiDiagram(resize_width, resize_height, num_of_points)
    vor.optimize()

    for group in vor.coor_groupings:
        num_of_coors = max(1, len(group))
        avg_red, avg_green, avg_blue = 0, 0, 0
        for coor in group:
            red, green, blue = image.getpixel(coor)
            avg_red += red
            avg_green += green
            avg_blue += blue

        avg_red /= num_of_coors
        avg_green /= num_of_coors
        avg_blue /= num_of_coors
        new_color = (round(avg_red), round(avg_green), round(avg_blue))

        for coor in group:
            draw.point(coor, new_color)

    return dummy_img


if __name__ == '__main__':
    img = multi_circles(500, 500, optimize=True)
    img.show()
    img.save("5.bmp", 'BMP')