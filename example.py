# -*- coding: utf-8

import random

from fixtures import get_person_data, MIN, MAX, get_cat_data
from memdb import Entity, measure


@measure
def populate(entity, fixture) -> None:
    total: int = random.choice(range(MIN, MAX))
    print(f'Loading {total} instances')
    for _ in range(total):
        entity.repository.add(next(fixture()))


@measure
def apply_filters(entity, filters) -> None:
    total: int = random.choice(range(MIN, MAX))
    print(f'FILTER\tApplying {total} filters')
    for _ in range(total):
        entity.repository.filter_by(random.choice(filters))


@measure
def apply_remove_filters(entity, filters) -> None:
    total: int = random.choice(range(MIN, MAX))
    print(f'DELETE\tApplying {total} filters')
    for _ in range(total):
        entity.repository.remove_by(random.choice(filters))


if __name__ == '__main__':
    Persons = Entity(name='Person', attrs='name age city')
    Cats = Entity(name='Cat', attrs='age name city favourite_food')

    # Apply complex data filters and measure execution time
    filters = [
        lambda x: x.name.lower().endswith('s'),
        lambda x: x.name.lower().startswith('a'),
        lambda x: x.id in range(MIN, MAX),
        lambda x: x.id in range(MIN, MAX) or x.city.lower() in ('Madrid', 'Barcelona'),
        lambda x: len(x.city.split()) == 1,
        lambda x: len([i for i in list(x.name)]) == 5 and sum(range(0, x.id)) == 7,
    ]

    populate(Persons, get_person_data)
    apply_filters(Persons, filters)
    apply_remove_filters(Persons, filters)

    populate(Cats, get_cat_data)
    apply_filters(Cats, filters)
    apply_remove_filters(Cats, filters)
