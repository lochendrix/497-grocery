# What to multiply by to convert to grams
CONVERSION_TO_G_MAP = {
    'mcg': 1e-6,
    'mg': 1e-3,
    'g': 1,
    'kg': 1e3,
    'oz': 28.3495,
    'lb': 453.592
}

# FIXME: Cannot handle "counts" of produce
def unit_conversion_factor(target, source):
    target = target.lower()
    source = source.lower()

    if (target not in CONVERSION_TO_G_MAP) or (source not in CONVERSION_TO_G_MAP):
        return 1

    # Currently converting source to grams
    current_factor = CONVERSION_TO_G_MAP[source]
    # Now converting to the target
    current_factor /= CONVERSION_TO_G_MAP[target]

    return current_factor




NUTRITION_CODES = {
    1087: 'Calcium',
    1089: 'Iron',
    1093: 'Sodium',
    1104: 'Vitamin A',
    1162: 'Vitamin C',
    1253: 'Cholesterol',
    1258: 'Saturated Fat',
    1003: 'Protein',
    1005: 'Carbohydrate',
    1008: 'Energy',
    2000: 'Total Sugars',
    1079: 'Dietary Fiber',
    1092: 'Potassium',
    1257: 'Trans Fat',
    1004: 'Total Fat',
}

DAILY_VALUE_TABLE = {
    "Added Sugar": [50, 'g'],
    "Calcium": [1300, 'mg'],
    "Cholesterol": [300, 'mg'],
    "Dietary Fiber": [28, 'g'],
    "Total Fat": [78, 'g'],
    "Iodine": [150, 'mcg'],
    "Iron": [18, 'mg'],
    "Potassium": [4700, 'mg'],
    "Protein": [50, 'g'],
    "Saturated Fat": [20, 'g'],
    "Sodium": [2300, 'mg'],
    "Carbohydrate": [275, 'g'],
    "Vitamin A": [2700, 'IU'],
    "Vitamin B6": [1.7, 'mg'],
    "Vitamin B12": [2.4, 'mcg'],
    "Vitamin C": [90, 'mg'],
    "Vitamin D": [200, 'mcg'],
    "Vitamin K": [120, 'mcg'],
    "Zinc": [11, 'mg'],
}

# "Good" components that are typically lacking in a poor diet
GREENS = ["Calcium", "Dietary Fiber", "Iron", "Potassium", "Protein",
    "Vitamin A", "Vitamin B6", "Vitamin B12", "Vitamin C", "Vitamin D",
    "Vitamin K", "Zinc"
]

# "Bad" components that are typically excessive in a poor diet
REDS = ["Added Sugar", "Cholesterol", "Total Fat", 
    "Saturated Fat", "Carbohydrate"
]


ITEMS_BY_NUTRITION = {
  "Calcium": [
    "Milk",
    "Cheese",
    "Yogurt",
    "Fortified Orange Juice",
    "Tofu"
  ],
  "Iron": [
    "Spinach",
    "Lentils",
    "Beef",
    "Shrimp",
    "Kidney Beans"
  ],
  "Sodium": [
    "Soy Sauce",
    "Canned Soup",
    "Pickles",
    "Olives",
    "Processed Meats"
  ],
  "Vitamin A": [
    "Carrots",
    "Sweet Potatoes",
    "Kale",
    "Spinach",
    "Butternut Squash"
  ],
  "Vitamin C": [
    "Oranges",
    "Strawberries",
    "Bell Peppers",
    "Broccoli",
    "Kiwi"
  ],
  "Cholesterol": [
    "Egg Yolks",
    "Shrimp",
    "Liver",
    "Butter",
    "Cheese"
  ],
  "Saturated Fat": [
    "Butter",
    "Coconut Oil",
    "Cheese",
    "Cream",
    "Red Meat"
  ],
  "Protein": [
    "Chicken Breast",
    "Tofu",
    "Greek Yogurt",
    "Eggs",
    "Salmon"
  ],
  "Carbohydrate": [
    "Bread",
    "Pasta",
    "Rice",
    "Potatoes",
    "Oats"
  ],
  "Energy": [
    "Peanut Butter",
    "Avocado",
    "Nuts",
    "Granola",
    "Bananas"
  ],
  "Total Sugars": [
    "Fruit Juice",
    "Candy",
    "Soda",
    "Desserts",
    "Sweetened Yogurt"
  ],
  "Dietary Fiber": [
    "Whole Grains",
    "Beans",
    "Berries",
    "Broccoli",
    "Nuts"
  ],
  "Potassium": [
    "Bananas",
    "Potatoes",
    "Spinach",
    "White Beans",
    "Avocado"
  ],
  "Trans Fat": [
    "Margarine",
    "Packaged Baked Goods",
    "Fried Foods",
    "Processed Snacks"
  ],
  "Total Fat": [
    "Avocado",
    "Nuts",
    "Olive Oil",
    "Salmon",
    "Cheese"
  ]
}

DEFAULT_SERVING_SIZES = {
    # Calcium
    "Milk": "240",
    "Cheese": "30",
    "Yogurt": "150",
    "Fortified Orange Juice": "240",
    "Tofu": "100",

    # Iron
    "Spinach": "85",          # cooked
    "Lentils": "100",         # cooked
    "Beef": "85",             # lean cut
    "Shrimp": "100",
    "Kidney Beans": "130",    # cooked

    # Sodium
    "Soy Sauce": "15",
    "Canned Soup": "250",
    "Pickles": "50",
    "Olives": "30",
    "Processed Meats": "85",

    # Vitamin A
    "Carrots": "80",
    "Sweet Potatoes": "130",
    "Kale": "67",
    "Spinach": "85",          # same as above
    "Butternut Squash": "200",

    # Vitamin C
    "Oranges": "130",
    "Strawberries": "150",
    "Bell Peppers": "75",
    "Broccoli": "85",
    "Kiwi": "75",

    # Cholesterol
    "Egg Yolks": "17",        # one egg yolk
    "Shrimp": "100",          # same as above
    "Liver": "85",
    "Butter": "14",
    "Cheese": "30",           # same as above

    # Saturated Fat
    "Butter": "14",           # same as above
    "Coconut Oil": "14",
    "Cheese": "30",           # same as above
    "Cream": "30",
    "Red Meat": "85",         # similar to Beef

    # Protein
    "Chicken Breast": "85",
    "Tofu": "100",            # same as above
    "Greek Yogurt": "150",
    "Eggs": "50",             # one whole egg
    "Salmon": "85",

    # Carbohydrate
    "Bread": "30",
    "Pasta": "56",            # dry weight per serving
    "Rice": "60",             # dry weight per serving
    "Potatoes": "150",
    "Oats": "40",

    # Energy
    "Peanut Butter": "32",
    "Avocado": "150",
    "Nuts": "28",
    "Granola": "50",
    "Bananas": "118",         # average small banana

    # Total Sugars
    "Fruit Juice": "240",
    "Candy": "40",
    "Soda": "355",
    "Desserts": "100",
    "Sweetened Yogurt": "150",

    # Dietary Fiber
    "Whole Grains": "40",
    "Beans": "130",
    "Berries": "150",
    "Broccoli": "85",         # same as above
    "Nuts": "28",             # same as above

    # Potassium
    "Bananas": "118",         # same as above
    "Potatoes": "150",        # same as above
    "Spinach": "8g",          # same as above
    "White Beans": "130",
    "Avocado": "15g",         # same as above

    # Trans Fat
    "Margarine": "14",
    "Packaged Baked Goods": "30",
    "Fried Foods": "100",
    "Processed Snacks": "28",

    # Total Fat
    "Avocado": "150",         # same as above
    "Nuts": "28",             # same as above
    "Olive Oil": "14",
    "Salmon": "85",           # same as above
    "Cheese": "30"            # same as above
}