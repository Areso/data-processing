# -*- encoding: utf-8 -*-

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json
import sys


def read_polygons(path_to_polygons, park=False):
    layer = "districts"
    if parks:
        layer = "parks"
    with open(path_to_polygons, encoding="utf-8") as file:
        print(layer)
        polygons = json.load(file)[layer]
        return {p["id"]: Polygon([(float(cords.split(', ')[1]), float(cords.split(', ')[0]))
                                  for cords in p["coords"]]) for p in polygons}


if __name__ == '__main__':
    #python3 app_intersects.py 56.8463371 60.6142361 1.0
    point = Point([float(sys.argv[-3]), float(sys.argv[-2])])
    parks = bool(float(sys.argv[-1]))
    path_to_polygons = "parks.json"
    polygons = read_polygons(path_to_polygons)
    found = False
    for polygon in polygons:
        if polygons[polygon].contains(point):
            print(polygon)
            found = True

    if not found:
        print(-1)


