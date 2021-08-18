from shapely import affinity
from shapely.geometry import box, MultiPolygon


if __name__ == '__main__':
    points = ((5, 5), (10, 5), (5, 10), (10, 10))

    polygons = MultiPolygon([
        affinity.rotate(
            box(p[0] - 2, p[1] - 1, p[0] + 2, p[1] + 1),
            30
        ) for p in points
    ])

    print(polygons.wkt)
    print(affinity.rotate(polygons, -30).wkt)
