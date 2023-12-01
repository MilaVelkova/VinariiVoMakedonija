from Model.Winery import Winery
import pandas as pd
import json


def instantiate_wineries():
    file = pd.read_csv("static/csv/final_scraped_wineries.csv", encoding='latin1')
    parsed_json = file.to_json(orient='records')
    parsed_json = json.loads(parsed_json)
    print(parsed_json)
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
