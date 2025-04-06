import requests
import json
import pandas as pd
import os


from dotenv import load_dotenv

load_dotenv()  # loads the variables from .env file


######################## STORE FINDER HANDLING ###########################
def Kroger_get_store_list(zip_code_str):
    auth = (
        os.getenv("KROGER_API_NAME"),
        os.getenv("KROGER_API_PW")
    )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    x = requests.post("https://api.kroger.com/v1/connect/oauth2/token", 
                      data={"grant_type": "client_credentials", "scope": "product.compact"},
                      headers=headers, auth=auth)
    token = x.json()['access_token']

    #zipcode_str = "48109"          # Example zipcode
    search_radius_miles = 20
    max_results = 200              # Maximum allowed
    chain = "Kroger"               # Chain filter

    headers = {"Authorization": "Bearer " + token}
    params = {
        "filter.zipCode.near": zip_code_str, 
        "filter.limit": max_results,
        "filter.radiusInMiles": search_radius_miles,
        "filter.chain": chain
    }
    resp = requests.get("https://api.kroger.com/v1/locations", headers=headers, params=params)
    
    stores = resp.json().get("data", [])
    output = f"Found {len(stores)} stores.\n"
    store_data = {}
    if stores:
        store_data = stores[0]
    else:
        store_data = "No stores found."
    
    return output, store_data


def Kroger_parse_stores_list(stores_list):
    return_dict = {}
    return_dict["ID"] = stores_list["locationId"]
    return_dict["street"] = stores_list["address"]["addressLine1"]
    return_dict["city"] = stores_list["address"]["city"]
    return return_dict



######################## PRODUCT FINDER HANDLING ###########################
# Example location ID: 01800605 (2641 Plymouth Road, Ann Arbor)
def Kroger_get_product_info(location_id, filter_term):
    auth = (
        os.getenv("KROGER_API_NAME"),
        os.getenv("KROGER_API_PW")
    )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    x = requests.post("https://api.kroger.com/v1/connect/oauth2/token", 
                      data={"grant_type": "client_credentials", "scope": "product.compact"},
                      headers=headers, auth=auth)
    token = x.json()['access_token']

    headers = {"Authorization": "Bearer " + token}
    params = {"filter.locationId": location_id, "filter.limit":1, "filter.term":filter_term}
    resp = requests.get("https://api.kroger.com/v1/products", headers=headers, params=params)
    
    product = resp.json()
    return product


def Kroger_parse_product(product):
    product_info = {}
    product_info['Name'] = product['description']
    product_info['Unit Price'] = product['items'][0]['price']['regular']
    size = (product['items'][0]['size']).split(" ")
    product_info['Unit Size'] = float(size[0])
    product_info['Unit Size units'] = size[1]
    product_info['Category'] = product['categories'][0]
    product_info['upcID'] = product['upc']
    product_info['image_url'] = product['images'][0]['sizes'][0]['url']
    product_info['store'] = 'Kroger'

    return product_info







# Ignore this -- sample API return
false = False
true = True
test = {
    "data": [
        {
            "productId": "0000000003107",
            "upc": "0000000003107",
            "productPageURI": "/p/fresh-navel-oranges-each/0000000003107?cid=dis.api.tpi_products-api_20240521_b:all_c:p_t:eecs497finalproject-",
            "aisleLocations": [
                {
                    "description": "PRODUCE",
                    "number": "0"
                }
            ],
            "brand": "Fresh Citrus",
            "categories": [
                "Produce",
                "Produce"
            ],
            "countryOrigin": "CHILE; MEXICO; SOUTH AFRICA; UNITED STATES",
            "description": "Fresh Navel Oranges - Each",
            "images": [
                {
                    "perspective": "back",
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/back/0000000003107"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/back/0000000003107"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/back/0000000003107"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/back/0000000003107"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/back/0000000003107"
                        }
                    ]
                },
                {
                    "perspective": "right",
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/right/0000000003107"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/right/0000000003107"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/right/0000000003107"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/right/0000000003107"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/right/0000000003107"
                        }
                    ]
                },
                {
                    "perspective": "front",
                    "featured": true,
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/front/0000000003107"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/front/0000000003107"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/front/0000000003107"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/front/0000000003107"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/front/0000000003107"
                        }
                    ]
                },
                {
                    "perspective": "left",
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/left/0000000003107"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/left/0000000003107"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/left/0000000003107"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/left/0000000003107"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/left/0000000003107"
                        }
                    ]
                }
            ],
            "items": [
                {
                    "itemId": "0000000003107",
                    "inventory": {
                        "stockLevel": "HIGH"
                    },
                    "favorite": false,
                    "fulfillment": {
                        "curbside": true,
                        "delivery": true,
                        "inStore": true,
                        "shipToHome": false
                    },
                    "price": {
                        "regular": 1.19,
                        "promo": 0
                    },
                    "size": "1 each",
                    "soldBy": "UNIT"
                }
            ],
            "itemInformation": {
                "depth": "3.1",
                "height": "3.1",
                "width": "3.1"
            },
            "temperature": {
                "indicator": "Ambient",
                "heatSensitive": false
            }
        },
        {
            "productId": "0001111065042",
            "upc": "0001111065042",
            "productPageURI": "/p/private-selection-sugar-gem-extra-sweet-navel-oranges/0001111065042?cid=dis.api.tpi_products-api_20240521_b:all_c:p_t:eecs497finalproject-",
            "aisleLocations": [
                {
                    "description": "PRODUCE",
                    "number": "0"
                }
            ],
            "categories": [
                "Produce"
            ],
            "countryOrigin": "UNITED STATES",
            "description": "Private Selection\u00ae Sugar Gem Extra Sweet Navel Oranges",
            "images": [
                {
                    "perspective": "back",
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/back/0001111065042"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/back/0001111065042"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/back/0001111065042"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/back/0001111065042"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/back/0001111065042"
                        }
                    ]
                },
                {
                    "perspective": "right",
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/right/0001111065042"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/right/0001111065042"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/right/0001111065042"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/right/0001111065042"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/right/0001111065042"
                        }
                    ]
                },
                {
                    "perspective": "front",
                    "featured": true,
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/front/0001111065042"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/front/0001111065042"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/front/0001111065042"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/front/0001111065042"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/front/0001111065042"
                        }
                    ]
                },
                {
                    "perspective": "left",
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/left/0001111065042"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/left/0001111065042"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/left/0001111065042"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/left/0001111065042"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/left/0001111065042"
                        }
                    ]
                },
                {
                    "perspective": "top",
                    "sizes": [
                        {
                            "size": "xlarge",
                            "url": "https://www.kroger.com/product/images/xlarge/top/0001111065042"
                        },
                        {
                            "size": "large",
                            "url": "https://www.kroger.com/product/images/large/top/0001111065042"
                        },
                        {
                            "size": "medium",
                            "url": "https://www.kroger.com/product/images/medium/top/0001111065042"
                        },
                        {
                            "size": "small",
                            "url": "https://www.kroger.com/product/images/small/top/0001111065042"
                        },
                        {
                            "size": "thumbnail",
                            "url": "https://www.kroger.com/product/images/thumbnail/top/0001111065042"
                        }
                    ]
                }
            ],
            "items": [
                {
                    "itemId": "0001111065042",
                    "inventory": {
                        "stockLevel": "HIGH"
                    },
                    "favorite": false,
                    "fulfillment": {
                        "curbside": true,
                        "delivery": true,
                        "inStore": true,
                        "shipToHome": false
                    },
                    "price": {
                        "regular": 4.99,
                        "promo": 0
                    },
                    "size": "4 ct",
                    "soldBy": "UNIT"
                }
            ],
            "itemInformation": {
                "depth": "6.5",
                "height": "3.0",
                "width": "6.5"
            },
            "temperature": {
                "indicator": "Refrigerated",
                "heatSensitive": false
            }
        }
    ],
    "meta": {
        "pagination": {
            "start": 0,
            "limit": 2,
            "total": 474
        }
    }
}