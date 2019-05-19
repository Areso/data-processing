#! -*- encoding: utf-8 -*-
import json
from typing import List, Union, Tuple
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class CityPolygon(object):
    def __init__(self, goejson_dict: dict):
        self.name: str = goejson_dict["properties"]["name"]
        self.id: int = goejson_dict["properties"]["id"]
        self.polygon: Polygon = Polygon([tuple(p) for p in goejson_dict["geometry"]["coordinates"][0][0]])
        self.area: float = goejson_dict["properties"]["area"]
        self.coords: List[List[float]] = goejson_dict["geometry"]["coordinates"][0][0]
        self.coords = ["%f, %f" % (self.coords[i][0], self.coords[i][1]) for i in range(len(self.coords))]
        self.objects_in_50: int = 0
        self.color: str = ''
        self.level: str = '' #added


    def intercepts(self, point_coordinates: Union[List[float], Tuple[float, float]]) -> bool:
        point = Point(point_coordinates[0], point_coordinates[1])
        if self.polygon.contains(point):
            return True
        return False

    def get_comfort_level(self) -> float:
        return self.objects_in_50 / self.area

if __name__ == '__main__':
    print("Hello world")
