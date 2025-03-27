import requests
import json
import pandas as pd
import os

from dotenv import load_dotenv

from utility import *

load_dotenv()  # loads the variables from .env file

def USDA_find_top_result_by_name(product_name):
    product_USDA_data = USDA_query_nutrition_of_item(product_name)
    if product_USDA_data['totalHits'] == 0:
        return -1

    return product_USDA_data['foods'][0]


def USDA_parse_nutrition_info(product_USDA_data):
    product_parsed = {}

    product_parsed['serving_size'] = product_USDA_data['servingSize']
    product_parsed['serving_size_unit'] = product_USDA_data['servingSizeUnit']


    nutrients_dict = {}
    product_nutrition = product_USDA_data['foodNutrients']
    for nutrient in product_nutrition:
        id = nutrient['nutrientId']
        if id not in NUTRITION_CODES:
            continue

        nutrients_dict[NUTRITION_CODES[id]] = {
            "value": nutrient['value'],
            "units": nutrient['unitName']
        }
    
    product_parsed['nutrients'] = nutrients_dict

    return product_parsed




# item_key could be a UPC key, a name, etc (anything that works in the USDA search bar)
def USDA_query_nutrition_of_item(item_key):
    auth = os.getenv("USDA_API_NAME")

    url_of_request = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=" + auth + "&query=" + str(item_key) + "" # Weird "" is needed
    resp = requests.get(url_of_request)
    info = resp.json()
    
    return info