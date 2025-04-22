import re
import logging
from utility import *
from functools import cmp_to_key

class Grocery_List:

    def __init__(self, grocery_list):
        self.list = grocery_list

    ##### Driver function for computing and ordering by scores #####
    def full_preparation(self):
        self.standardize_weight_units()
        self.standardize_serving_size()
        self.convert_to_DV()
        self.health_score_groceries()
        self.cost_score_groceries()
        self.order_groceries_by_score()

    # Convert several measurements to grams
    def standardize_weight_units(self):
        for i in range(len(self.list)):
            unit_size_conv_factor = unit_conversion_factor('g', self.list[i]['Unit Size units'])
            self.list[i]['Unit Size'] *= unit_size_conv_factor
            self.list[i]['Unit Size units'] = 'g'
            
            unit_size_conv_factor = unit_conversion_factor('g', self.list[i]['serving_size_unit'])
            self.list[i]['serving_size'] *= round(unit_size_conv_factor)
            self.list[i]['serving_size_unit'] = 'g'

            for key in self.list[i]['nutrients']:
                if key not in DAILY_VALUE_TABLE:
                    continue
                target_unit = DAILY_VALUE_TABLE[key][1]
                unit_size_conv_factor = unit_conversion_factor(target_unit, self.list[i]['nutrients'][key]['units'])
                self.list[i]['nutrients'][key]['value'] *= unit_size_conv_factor
                self.list[i]['nutrients'][key]['units'] = target_unit

    # Standardize to 100 grams, scaling all nutrititon counts accordingly
    def standardize_serving_size(self):
        for i in range(len(self.list)):
            # What to multiply by
            serving = self.list[i]['serving_size']
            logging.debug(self.list[i])
            if isinstance(serving, (int, float)):
                numeric_serving = serving
            else:
                numeric_serving = int(re.sub(r'\D', '', serving))
            if numeric_serving == 0:
                numeric_serving = 100.0  # Default to 100g if serving size is not a number
            scale_factor = 100.0 / numeric_serving
            self.list[i]['serving_size'] = 100.0

            for key in self.list[i]['nutrients']:
                self.list[i]['nutrients'][key]['value'] *= scale_factor

    # Converts nutrient amounts to %DV
    def convert_to_DV(self):
        for i in range(len(self.list)):
            for key in self.list[i]['nutrients']:
                if key not in DAILY_VALUE_TABLE:
                    continue
                self.list[i]['nutrients'][key]['value'] *= 100
                self.list[i]['nutrients'][key]['value'] /= DAILY_VALUE_TABLE[key][0]
                self.list[i]['nutrients'][key]['units'] = '%DV'


    # Insert a health score for each grocery
    def health_score_groceries(self):
        min_score =  999999
        max_score = -999999
        for i in range(len(self.list)):
            green_score = get_filtered_DV_sum_of_product(self.list[i]['nutrients'], GREENS)
            # FIXME: I'm testing out removing the reds; they reduce the score too much, 
            # and unhealthy things don't have enough greens to increase their score much anyways
            #red_score = get_filtered_DV_sum_of_product(self.list[i]['nutrients'], REDS)
            self.list[i]['health_score'] = green_score# - red_score
            if self.list[i]['health_score'] < min_score:
                min_score = self.list[i]['health_score']
            if self.list[i]['health_score'] > max_score:
                max_score = self.list[i]['health_score']
        
        # Adjust scores
        #for i in range(len(self.list)):
        #    self.list[i]['health_score'] -= min_score # Sets min to 0
        for i in range(len(self.list)):
            self.list[i]['health_score'] /= max_score # Scales to [0, 1]

    # Insert a cost (health adjusted) score for each grocery
    # NOTE: ONLY CALL AFTER health_score_groceries
    def cost_score_groceries(self):
        for i in range(len(self.list)):
            # number of 100g servings
            multiplier = self.list[i]['Unit Size'] / 100
            score = multiplier * self.list[i]['health_score']

            # Cost divider
            score /= self.list[i]['Unit Price']

            self.list[i]['cost_score'] = score

    # Highest score goes first
    def order_groceries_by_score(self):
        self.list = sorted(self.list, key=cmp_to_key(comp_scores))


    ##### Prepares JSON/dict for the JS page
    def prep_JSON_for_webpage(self):
        self.grab_3_nutrition_highlights()

        json_list = []
        for i in range(len(self.list)):
            json_list.append(self.make_JS_entry_from_list_entry(i))
        
        return json_list

    def grab_3_nutrition_highlights(self):
        for i in range(len(self.list)):
            nutrition_dv_pairs = []
            for key in GREENS:
                if key not in self.list[i]['nutrients']:
                    continue
                val = self.list[i]['nutrients'][key]['value']
                if val == 0:
                    continue
                nutrition_dv_pairs.append([key, val])
        
            nutrition_dv_pairs = sorted(nutrition_dv_pairs, key=cmp_to_key(comp_nutrition))
            if len(nutrition_dv_pairs) > 3:
                nutrition_dv_pairs = nutrition_dv_pairs[:3]
            self.list[i]['highlights'] = nutrition_dv_pairs
    
    def make_JS_entry_from_list_entry(self, idx):
        js_entry = {
            "Store name": self.list[idx]['store'],
            "Product name": self.list[idx]["Name"],
            "image": self.list[idx]["image_url"],
            "Product cost": self.list[idx]["Unit Price"],
            "Health score": self.list[idx]["health_score"],
            "Cost score": self.list[idx]["cost_score"],
            "Nutrititon highlights": self.list[idx]['highlights'],
            "upcID": self.list[idx]['upcID'],
            "Street": self.list[idx]['Street'],
            "City": self.list[idx]['City']
        }
        return js_entry






# HELPER
def get_filtered_DV_sum_of_product(product_nutrients, list_of_nutrients):
    sum = 0
    for nutrient in list_of_nutrients:
        if nutrient not in DAILY_VALUE_TABLE:
            continue
        if nutrient in product_nutrients:
            sum += product_nutrients[nutrient]['value']

    return sum

# HELPER - custom comparator for sorting:
def comp_scores(item1, item2):
    item1_score = item1['health_score'] + item1['cost_score']
    item2_score = item2['health_score'] + item2['cost_score']

    return item2_score - item1_score

def comp_nutrition(item1, item2):
    return item2[1] - item1[1]