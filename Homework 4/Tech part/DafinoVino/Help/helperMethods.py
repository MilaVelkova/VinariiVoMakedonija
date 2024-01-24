import pandas as pd
import json
import sys
import os
from math import radians, sin, cos, sqrt, atan2
sys.path.append(os.getcwd())
from app_models.Winery import Winery

def return_json_wineries():
    file = pd.read_csv("static/csv/final_scraped_wineries.csv", encoding='latin1')
    parsed_json = file.to_json(orient='records')
    parsed_json = json.loads(parsed_json)
    return parsed_json


def instantiate_wineries():
    file = pd.read_csv("static/csv/final_scraped_wineries.csv", encoding='latin1')
    parsed_json = file.to_json(orient='records')
    parsed_json = json.loads(parsed_json)
    # print(parsed_json)
    new_list = list()
    i = 0
    for item in parsed_json:
        new_list.append(Winery(i,
                               item['Winary Name'],
                               item['Winary Description'],
                               item['Winary Image Link'],
                               item['Winary Rating'],
                               item['Winary Location']))
        i += 1
    return new_list


def find_winery_by_id(list_to_search, id):
    list_found = [item for item in list_to_search if item.id == id]
    return list_found[0]


def winery_repository():
    return instantiate_wineries()


def find_winery_by_id_ser(list_to_search, id):
    return find_winery_by_id(list_to_search, id)



def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate the differences between latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance