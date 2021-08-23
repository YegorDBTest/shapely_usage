from operator import attrgetter

from statistics import fmean

from shapely import affinity
from shapely.geometry import box, MultiPolygon


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

    def get_lines(self):
        coords = tuple(self.polygon.boundary.coords)
        lines = [GeomLine(coords[i : i + 2]) for i in range(4)]
        return {
            'back': min(*lines),
            'front': max(*lines),
        }


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
    # print(rotated_mp.wkt)

    for i, pg in enumerate(rotated_mp.geoms):
        items[i].polygon = pg

    for item in sorted(items):
        # print(item.polygon.wkt)
        lines = item.get_lines()
        print('back', lines['back'].points)
        print('front', lines['front'].points)
