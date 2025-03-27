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
    "Protein": [
        "Chicken Breast",
        "Turkey Breast",
        "Tofu",
        "Salmon",
        "Greek Yogurt",
        "Eggs"
    ],
    "Calcium": [
        "Milk",
        "Cheese",
        "Yogurt",
        "Kale",
        "Almonds"
    ],
    "Iron": [
        "Spinach",
        "Lentils",
        "Beef",
        "Kidney Beans"
    ],
    "Sodium": [
        "Soy Sauce",
        "Canned Soup",
        "Pickles",
        "Pretzels"
    ],
    "Vitamin A": [
        "Carrots",
        "Sweet Potatoes",
        "Butternut Squash",
        "Kale"
    ],
    "Cholesterol": [
        "Eggs",
        "Shrimp",
        "Liver",
        "Butter"
    ],
    "Saturated Fat": [
        "Butter",
        "Coconut Oil",
        "Cheese",
        "Cream"
    ],
    "Carbohydrate": [
        "Bread",
        "Pasta",
        "Rice",
        "Oats"
    ],
    "Energy": [
        "Peanut Butter",
        "Avocado",
        "Nuts",
        "Granola"
    ],
    "Total Sugars": [
        "Candy",
        "Fruit Juice",
        "Soft Drinks",
        "Syrup"
    ],
    "Dietary Fiber": [
        "Broccoli",
        "Chia Seeds",
        "Berries",
        "Whole Grain Bread"
    ],
    "Potassium": [
        "Bananas",
        "White Beans",
        "Avocado",
        "Potatoes"
    ],
    "Trans Fat": [
        "Margarine",
        "Shortening",
        "Fried Foods"
    ]
}