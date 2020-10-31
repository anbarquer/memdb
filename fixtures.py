# -*- coding: utf-8

import random
from typing import List, Generator, Dict

_NAMES: List[str] = [
    'Liam',
    'Olivia',
    'Noah',
    'Emma',
    'Amelia',
    'Oliver',
    'Lucas',
    'Isabella',
    'William',
    'Evelyn',
    'Anthony',
    'Bernard'
]

_CITIES: List[str] = [
    'Barcelona',
    'London',
    'Indianapolis',
    'Berlin',
    'Sydney',
    'Indianapolis',
    'Andorra',
    'Irvine',
    'Irving',
    'Barakī',
    'Malanje',
    'Madrid',
    'Mallorca',
    'Rome'
]

_FAVOURITE_FOOD: List[str] = [
    'Pasta',
    'Ice Cream',
    'Bread',
    'Pizza',
    'Banana',
    'Cheese',
    'Potato Chips',
    'Tacos',
    'Burrito',
    'Broccoli',
    'Apple',
    'Orange',
    'Chicken Nuggets'
]

MIN, MAX = 10000, 100000


def get_person_data() -> Generator[Dict, None, None]:
    min_person, max_person = 1, 99
    while True:
        yield {
            'name': random.choice(_NAMES),
            'age': random.choice(range(min_person, max_person)),
            'city': random.choice(_CITIES)
        }


def get_cat_data() -> Generator[Dict, None, None]:
    min_cat, max_cat = 1, 20
    while True:
        yield {
            'name': random.choice(_NAMES),
            'age': random.choice(range(min_cat, max_cat)),
            'favourite_food': random.choice(_FAVOURITE_FOOD),
            'city': random.choice(_CITIES)
        }
