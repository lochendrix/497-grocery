import logging
from services.kroger import *
from services.usda import *

from utility import *

from grocery_data_frontend_algs import *

# location_id is a Kroger store ID
# Product name is a simple name, like "Chicken" (although more detailed names could work)
def Kroger_find_product(location_id, product_name):
    # Find a Kroger product with the basic name -- likely has no USDA data
    product_info = Kroger_get_product_info(location_id, product_name)
    # Grab the brand name of the top result
    product_brand = product_info['data'][0]['brand']

    # Search that product name with brand on USDA to get a result 
    # likely DOES have a Kroger entry
    query = f"{product_brand} {product_name}"
    logging.debug(f"USDA query: {query}")
    product_USDA_info = USDA_find_top_result_by_name(query)
    logging.debug(f"USDA info got: {product_USDA_info}")

     # If the USDA search returns nothing, try with just the product name
    if not product_USDA_info:
        logging.debug("USDA query with brand returned no result. Trying with product name only.")
        product_USDA_info = USDA_find_top_result_by_name(product_name)
    # Find the corresponding Kroger entry
    product_info = Kroger_get_product_info(location_id, product_USDA_info['description'])

    # Return the pair of [Kroger API, USDA API] returns for the product
    return [product_info['data'][0], product_USDA_info]

# Parse through Kroger and USDA API returns to get final info for one product
def Kroger_get_final_product_info(location_id, product_name):
    try:
        product_info = Kroger_find_product(location_id, product_name)
        product_info_kroger = Kroger_parse_product(product_info[0])
        product_info_USDA = USDA_parse_nutrition_info(product_info[1])
        product_info = product_info_kroger | product_info_USDA

        return product_info
    except:
        logging.exception("An error occurred while trying to get final product info.")
        return -1

# Get final info for a bunch of groceries
def Kroger_get_grocery_list(location_id, nutrititon_type=None):
    grocery_list = []
    # If the user specified a nutritition type
    if nutrititon_type in ITEMS_BY_NUTRITION:
        for grocery in ITEMS_BY_NUTRITION[nutrititon_type]:
            grocery_info = Kroger_get_final_product_info(location_id, grocery)
            if grocery_info != -1:
                grocery_list.append(grocery_info)
    # If the user didn't specify a nutritition type
    else:
        for nutrient in ITEMS_BY_NUTRITION:
            for grocery in ITEMS_BY_NUTRITION[nutrient]:
                grocery_info = Kroger_get_final_product_info(location_id, grocery)
                if grocery_info != -1:
                    grocery_list.append(grocery_info)
    
    return Grocery_List(grocery_list)