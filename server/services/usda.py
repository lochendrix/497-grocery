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


def parse_serving_size(product_USDA_data):
    # Try to get the serving size directly
    serving_size = product_USDA_data.get('servingSize')
    if serving_size:
        return serving_size

    # Fallback: attempt to use foodMeasures if available
    if 'foodMeasures' in product_USDA_data and product_USDA_data['foodMeasures']:
        # Use the gram weight of the first measure as the serving size
        return f"{product_USDA_data['foodMeasures'][0]['gramWeight']}g"
    
    # Fallback: try to determine serving size based on the food category
    food_category = product_USDA_data.get('foodCategory', '')
    for item, default_size in DEFAULT_SERVING_SIZES.items():
        if item.lower() in food_category.lower():
            return default_size

    # Last resort: return a generic default
    return "100g"

def parse_serving_size_unit(product_USDA_data):
    # Try to get the unit directly
    unit = product_USDA_data.get('servingSizeUnit')
    if unit:
        return unit
    
    # Fallback: if foodMeasures exist, try using the first measure's unitName
    if 'foodMeasures' in product_USDA_data and product_USDA_data['foodMeasures']:
        return product_USDA_data['foodMeasures'][0].get('unit', "g")
    
    # Last resort: default unit
    return "g"


def USDA_parse_nutrition_info(product_USDA_data):
    product_parsed = {}

    product_parsed['serving_size'] = parse_serving_size(product_USDA_data)
    product_parsed['serving_size_unit'] = parse_serving_size_unit(product_USDA_data)

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