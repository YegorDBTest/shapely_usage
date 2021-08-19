from operator import attrgetter

from statistics import fmean

from shapely import affinity
from shapely.geometry import box, MultiPolygon


class Geom:

    def __init__(self, x, y, width, height, angle):
        self.angle = angle
        self.polygon = affinity.rotate(
            box(x - width / 2, y - height / 2, x + width / 2, y + height / 2),
            angle
        )


if __name__ == '__main__':
    items = (
        Geom(5, 5, 4, 2, 30.0),
        Geom(10, 5, 4, 2, 31.6),
        Geom(5, 10, 4, 2, 28.2),
        Geom(10, 10, 4, 2, 36.7),
    )

    polygons = MultiPolygon(map(attrgetter('polygon'), items))

    average_angle = fmean(map(attrgetter('angle'), items))

    print(polygons.wkt)
    print(affinity.rotate(polygons, -average_angle).wkt)
