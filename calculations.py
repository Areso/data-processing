#! -*- encoding: utf-8 -*-
import json
from Polygon import CityPolygon
from typing import List, Dict
from math import sin, cos, sqrt, atan2, radians
import os
import pandas


GOOD_CONST = 10

def street_len(geo_coords: List[List[float]]) -> float:
    """
    Takes a list of a street's coordinates [lat, lon] and calculates the length of the street
    :param geo_coords: List of latitudes and longitudes of the street
    :return: Length of the street
    """
    if len(geo_coords) < 2:
        return 0.0
    street_length = 0.0
    # approximate radius of earth in km
    R = 6373.0
    for i in range(len(geo_coords) - 1):
        lat1 = radians(geo_coords[i][0])
        lon1 = radians(geo_coords[i][1])
        lat2 = radians(geo_coords[i + 1][0])
        lon2 = radians(geo_coords[i + 1][1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        street_length += distance
    return street_length


def streets_dict(path_to_geojson: str) -> Dict[str, float]:
    """
    Reads a geojson file with all streets
    :param path_to_geojson: Path to a geojson file
    :return: Dict with streets' names as key and streets' lengths as values
    """
    street_dicts = {}
    with open(path_to_geojson, encoding="utf-8") as file:
        streets = json.load(file)["features"]
        for s in streets:
            if s["properties"]["NAME"] not in street_dicts:
                street_dicts[s["properties"]["NAME"]] = street_len(s["geometry"]["coordinates"][0])
            else:
                street_dicts[s["properties"]["NAME"]] += street_len(s["geometry"]["coordinates"][0])

    street_dicts.pop("Подъезд к п. Палкинский торфяник")
    street_dicts.pop("ЕКАД")
    street_dicts.pop("Пермь — Екатеринбург")
    street_dicts.pop("г. Екатеринбург – г. Первоуральск")
    street_dicts.pop("Екатеринбургская кольцевая автомобильная дорога")
    street_dicts.pop("Подъезд к оз. Глухое")
    street_dicts.pop("Подъезд к п. Палкинский торфяник от км 9+470 а/д «г. Екатеринбург — г. Первоуральск»")
    street_dicts.pop("Чусовской тракт")
    street_dicts.pop("Подъезд к п. Шабровский от км 17+420 а/д «г. Екатеринбург — г. Полевской»")
    street_dicts.pop("г. Екатеринбург – с. Косулино")
    street_dicts.pop("п. Северка — п. Палкино")
    street_dicts.pop("г. Екатеринбург — г. Реж — г. Алапаевск")
    street_dicts.pop("Подъезд к посёлку 9 км от км 354+000 а/д «г. Пермь — г. Екатеринбург»")
    street_dicts.pop("г. Екатеринбург — г. Нижний Тагил — г. Серов")
    street_dicts.pop("г. Екатеринбург — г. Полевской")
    street_dicts.pop("г. Екатеринбург — аэропорт «Кольцово»")
    return street_dicts


def streets_in_districts(districts: List[CityPolygon], path_to_streets: str) -> Dict[str, List[str]]:
    city_polygons = {district.name: district for district in districts}

    district_streets = {polygon_name: [] for polygon_name in city_polygons}
    with open(path_to_streets, encoding="utf-8") as file:
        streets = json.load(file)["features"]
        for street in streets:
            # print("Working")
            street_points = street["geometry"]["coordinates"][0]
            for point in street_points:
                for polygon in city_polygons:
                    if city_polygons[polygon].intercepts(point):
                        if street["properties"]["NAME"] not in district_streets[polygon]:
                            district_streets[polygon].append(street["properties"]["NAME"])
                            break

    return district_streets


def goods_at_street(path_to_goods: str, streets: Dict[str, int], green_areas: List[CityPolygon]):
    goods = pandas.read_csv(path_to_goods, encoding="utf8", sep=';')
    address = goods["Адрес"].values
    latitudes = goods["latitude"].values
    longitudes = goods["longitude"].values
    for i in range(len(address)):
        for k in range(len(green_areas)):
            if green_areas[k].intercepts([latitudes[i], longitudes[i]]):
                green_areas[k].objects_in_50 += 1

        if address[i] != '':
            ad = address[i].split(', ')
            for a in ad:
                for street in streets:
                    if a in street:
                        streets[street] += 1


def district_json(id: int, district: CityPolygon, district_streets: List[str], good_streets: List[str]):
    all_streets = len(district_streets)
    good_count = len([s for s in district_streets if s in good_streets])
    color = "#ff0000"
    if good_count / all_streets > 0.5:
        color = "#ffff00"
        if good_count / all_streets > 0.7:
            color = "#00ff00"

    json_dict = {"id": "%d" % id,
                 "name": "%s" % district.name,
                 "area": "%.3f" % district.area,
                 "streets": "%d" % all_streets,
                 "color": "%s" % color,
                 "goodstreets": "%d" % good_count,
                 "coords": district.coords}

    return json_dict


def district_list(path_to_districts: str) -> List[CityPolygon]:
    districts = []
    with open(path_to_districts, encoding="utf-8") as file:
        jdict = json.load(file)["features"]
        for district in jdict:
            districts.append(CityPolygon(district))
    return districts


def green_list(path_to_greens: str) -> List[CityPolygon]:
    greens = []
    with open(path_to_greens, encoding="utf-8") as file:
        jdict = json.load(file)["features"]
        for green in jdict:
            greens.append(CityPolygon(green))
    return greens


def park_list(path_to_parks: str) -> List[CityPolygon]:
    parks = []
    with open(path_to_parks, encoding="utf-8") as file:
        jdict = json.load(file)["features"]
        for park in jdict:
            parks.append(CityPolygon(park))
    return parks


def parks_geojson(parks: List[CityPolygon]) -> Dict[str, list]:
    jsoned = {"parks": []}
    for park in parks:
        jsoned["parks"].append({"id": "%d" % park.id,
                                "name": "%s" % park.name,
                                "area": "%.3f" % park.area,
                                "services": "%d" % park.objects_in_50,
                                "color": "%s" % park.color,
                                "coords": park.coords})
    return jsoned


if __name__ == '__main__':
    path_to_streets = "highway-line_ekb_str.geojson"  # Streets
    path_to_districts = "city_parts.geojson"  # Districts polygons
    path_to_parks = "parks.geojson"  # Parks (would be used at the app) (smaller)
    path_to_greens = "green_areas.geojson"  # Used to calculate park level's (larger)
    path_to_goods = "goods"  # Path to the folder with all goods

    districts = district_list(path_to_districts)
    greens = green_list(path_to_greens)
    parks = park_list(path_to_parks)
    district_streets = streets_in_districts(districts, path_to_streets)
    street_lengths = streets_dict(path_to_streets)
    street_goods = {street: 0 for street in street_lengths}
    path_to_goods = [os.path.join(path_to_goods, path) for path in os.listdir(path_to_goods)
                     if os.path.isfile(os.path.join(path_to_goods, path))]

    for path_to_good in path_to_goods:
        goods_at_street(path_to_good, street_goods, greens)

    comfort_levels = []
    for green in greens:
        for i in range(len(parks)):
            if parks[i].id == green.id:
                parks[i].objects_in_50 = green.objects_in_50
                comfort_levels.append(parks[i].get_comfort_level())
                break

    comfort_levels = sorted(comfort_levels)
    top_comfort = comfort_levels[-1]
    bottom_comfort = comfort_levels[0]
    comfort_range = top_comfort - bottom_comfort
    level1 = bottom_comfort
    level2 = level1 + 0.25 * comfort_range
    level3 = level2 + 0.25 * comfort_range
    level4 = level3 + 0.25 * comfort_range
    level5 = top_comfort

    park_colors = ["#ff80000", "#ffd500", "#ffff00", "#00ff00"]

    for i in range(len(parks)):
        parks[i].color = park_colors[0]
        if parks[i].get_comfort_level() > level4:
            parks[i].color = park_colors[3]
        elif parks[i].get_comfort_level() > level3:
            parks[i].color = park_colors[2]
        elif parks[i].get_comfort_level() > level2:
            parks[i].color = park_colors[1]

    park_jsoned = parks_geojson(parks)
    with open("parks.json", encoding="utf-8", mode='w') as outfile:
        json.dump(park_jsoned, outfile, ensure_ascii=False)

    exit(0)

    good_streets = [street for street in street_lengths if street_goods[street] / street_lengths[street] > GOOD_CONST]

    json_districts = {"districts": []}

    i = 1
    for district in districts:
        json_districts["districts"].append(district_json(i, district, district_streets[district.name], good_streets))
        i += 1

    with open("districts.json", encoding="utf-8", mode='w') as outfile:
        json.dump(json_districts, outfile, ensure_ascii=False)

    print("completed!")
