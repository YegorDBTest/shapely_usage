import math

from operator import attrgetter

from statistics import fmean

from shapely import affinity
from shapely.geometry import box, Polygon, MultiPolygon


class GeomLine:

    def __init__(self, points):
        self.points = points

    def __gt__(self, other):
        sum1 = self.points[0][0] + self.points[1][0]
        sum2 = other.points[0][0] + other.points[1][0]
        return sum1 > sum2

    def __eq__(self, other):
        sum1 = self.points[0][0] + self.points[1][0]
        sum2 = other.points[0][0] + other.points[1][0]
        return sum1 == sum2


class Geom:

    def __init__(self, x, y, width, height, angle):
        self.angle = angle
        self.polygon = affinity.rotate(
            box(x - width / 2, y - height / 2, x + width / 2, y + height / 2),
            angle
        )

    def __gt__(self, other):
        return (
            self.polygon.bounds[0] > other.polygon.bounds[2]
            or self.polygon.bounds[2] > other.polygon.bounds[0]
            and self.polygon.bounds[3] < other.polygon.bounds[1]
        )

    def __eq__(self, other):
        return (
            self.polygon.bounds[0] == other.polygon.bounds[0]
            and self.polygon.bounds[1] == other.polygon.bounds[1]
        )

    def get_front_polygon(self, right_border):
        coords = tuple(self.polygon.boundary.coords)
        front_line = max(*(GeomLine(coords[i : i + 2]) for i in range(4)))
        p1, p2 = front_line.points
        if self.angle == 0:
            p3 = (right_border, p2[1])
            p4 = (right_border, p1[1])
        else:
            tan = math.tan(math.radians(90 - self.angle))
            p3 = (right_border, p2[1] + ((right_border - p2[0]) / tan))
            p4 = (right_border, p1[1] + ((right_border - p1[0]) / tan))
        return Polygon([p1, p2, p3, p4])


if __name__ == '__main__':
    items = (
        Geom(2, 5, 4, 2, 30.0),
        Geom(10, 5, 4, 2, 31.6),
        Geom(2, 10, 4, 2, 28.2),
        Geom(10, 10, 4, 2, 36.7),
    )

    mp = MultiPolygon(map(attrgetter('polygon'), items))
    average_angle = fmean(map(attrgetter('angle'), items))
    rotated_mp = affinity.rotate(mp, -average_angle)
    print(rotated_mp.wkt)

    right_border = rotated_mp.bounds[3]

    for i, pg in enumerate(rotated_mp.geoms):
        items[i].polygon = pg
        items[i].angle -= average_angle

    front_polygons = []
    for item in sorted(items):
        front_polygons.append(item.get_front_polygon(right_border))
    front_polygons_mp = MultiPolygon(front_polygons)
    print(front_polygons_mp.wkt)
