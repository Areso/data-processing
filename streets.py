#! -*- encoding: utf-8 -*-
import json
from typing import List, Dict
from math import sin, cos, sqrt, atan2, radians


def street_len(geo_coords: List[List[float]]) -> float:
    """
    Takes a list of a street's coordinates [lat, lon] and calculates the length of the street
    :param geo_coords: List of latitudes and longitudes of the street
    :return: Length of the street
    """
    if len(geo_coords) < 2:  # If a street has less than two points - it has length 0
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


if __name__ == '__main__':
    path_to_streets = "highway-line_ekb_str.geojson"
    streets = streets_dict(path_to_streets)
    for s in streets:
        print(s, streets[s])
