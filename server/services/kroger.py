import requests
import json
import pandas as pd
import os


from dotenv import load_dotenv

load_dotenv()  # loads the variables from .env file

import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # loads the variables from .env file

def get_store_info():
    auth = (
        os.getenv("KROGER_API_NAME"),
        os.getenv("KROGER_API_PW")
    )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    x = requests.post("https://api.kroger.com/v1/connect/oauth2/token", 
                      data={"grant_type": "client_credentials", "scope": "product.compact"},
                      headers=headers, auth=auth)
    token = x.json()['access_token']

    zipcode_str = "48109"          # Example zipcode
    search_radius_miles = 20
    max_results = 200              # Maximum allowed
    chain = "Kroger"               # Chain filter

    headers = {"Authorization": "Bearer " + token}
    params = {
        "filter.zipCode.near": zipcode_str, 
        "filter.limit": max_results,
        "filter.radiusInMiles": search_radius_miles,
        "filter.chain": chain
    }
    resp = requests.get("https://api.kroger.com/v1/locations", headers=headers, params=params)
    
    stores = resp.json().get("data", [])
    output = f"Found {len(stores)} stores.\n"
    if stores:
        output += json.dumps(stores[0], indent=4)
    else:
        output += "No stores found."
    
    return output
