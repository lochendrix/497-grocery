import logging
from services.kroger import *
from services.usda import *

from utility import *

from grocery_data_frontend_algs import *

import threading

SHARED_DATA_LOCK = threading.Lock()
GROCERY_LIST_GLOBAL = {}

# location_id is a Kroger store ID
# Product name is a simple name, like "Chicken" (although more detailed names could work)
def Kroger_find_product(location_id, product_name):
    # Find a Kroger product with the basic name -- likely has no USDA data
    product_info = Kroger_get_product_info(location_id, product_name)
    # Grab the brand name of the top result
    product_brand = "Kroger"
    try:
        product_brand = product_info['data'][0]['brand']
    except:
        pass

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
def Kroger_get_final_product_info(store_info, product_name):
    try:
        product_info = Kroger_find_product(store_info['ID'], product_name)
        product_info_kroger = Kroger_parse_product(product_info[0])
        product_info_USDA = USDA_parse_nutrition_info(product_info[1])
        product_info = product_info_kroger | product_info_USDA
        product_info['Street'] = store_info['street']
        product_info['City'] = store_info['city']

        SHARED_DATA_LOCK.acquire()
        #print("\n\n\n\n LOCKED \n\n\n\n")
        #print(product_info)
        #GROCERY_LIST_GLOBAL.append(product_info)
        try:
            GROCERY_LIST_GLOBAL[product_info['upcID']] = product_info
            SHARED_DATA_LOCK.release()
        except:
            SHARED_DATA_LOCK.release()
        #print("\n\n\n\n UNLOCKED \n\n\n\n")
        #return product_info
    except:
        logging.exception("An error occurred while trying to get final product info.")
        return -1

# Get final info for a bunch of groceries
def Kroger_get_grocery_list(store_info, nutrititon_type=None):
    # Reset
    global GROCERY_LIST_GLOBAL
    GROCERY_LIST_GLOBAL = {}

    # Tracking threads
    grocery_info_threads = []

    # If the user specified a nutritition type
    if nutrititon_type in ITEMS_BY_NUTRITION:
        for grocery in ITEMS_BY_NUTRITION[nutrititon_type]:
            grocery_info_threads.append(
                threading.Thread(
                    target=Kroger_get_final_product_info, args=(store_info, grocery)
                )
            )
            grocery_info_threads[-1].start()
            #grocery_info = Kroger_get_final_product_info(store_info, grocery)
            #if grocery_info != -1:
            #    GROCERY_LIST_GLOBAL.append(grocery_info)
    # If the user didn't specify a nutritition type
    else:
        for nutrient in ITEMS_BY_NUTRITION:
            for grocery in ITEMS_BY_NUTRITION[nutrient]:
                grocery_info_threads.append(
                    threading.Thread(
                        target=Kroger_get_final_product_info, args=(store_info, grocery)
                    )
                )
                grocery_info_threads[-1].start()
    
    for t in grocery_info_threads:
        t.join()

    grocery_list_new = []
    for key in GROCERY_LIST_GLOBAL:
        grocery_list_new.append(GROCERY_LIST_GLOBAL[key])
    return Grocery_List(grocery_list_new)
'''

def Kroger_get_final_product_info(store_info, product_name):
    try:
        product_info = Kroger_find_product(store_info['ID'], product_name)
        product_info_kroger = Kroger_parse_product(product_info[0])
        product_info_USDA = USDA_parse_nutrition_info(product_info[1])
        product_info = product_info_kroger | product_info_USDA
        product_info['Street'] = store_info['street']
        product_info['City'] = store_info['city']

        return product_info
    except:
        logging.exception("An error occurred while trying to get final product info.")
        return -1

def Kroger_get_grocery_list(store_info, nutrititon_type=None):
    grocery_list = {}
    # If the user specified a nutritition type
    if nutrititon_type in ITEMS_BY_NUTRITION:
        for grocery in ITEMS_BY_NUTRITION[nutrititon_type]:
            grocery_info = Kroger_get_final_product_info(store_info, grocery)
            if grocery_info != -1:
                grocery_list[grocery_info['upcID']] = grocery_info
    # If the user didn't specify a nutritition type
    else:
        for nutrient in ITEMS_BY_NUTRITION:
            for grocery in ITEMS_BY_NUTRITION[nutrient]:
                grocery_info = Kroger_get_final_product_info(store_info, grocery)
                if grocery_info != -1:
                    grocery_list[grocery_info['upcID']] = grocery_info
    
    grocery_list_new = []
    for key in grocery_list:
        grocery_list_new.append(grocery_list[key])
    return Grocery_List(grocery_list_new)
'''