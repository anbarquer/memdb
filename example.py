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
    print(f'Applying {total} filters')
    for _ in range(total):
        entity.repository.filter_by(random.choice(filters))


if __name__ == '__main__':
    Persons = Entity(model='Person', attrs='name age city')

    Persons.repository.add({'name': 'This is a test', 'age': 23, 'city': 'Neverland'})
    print('Filter using Python lambda functions', Persons.repository.filter_by(lambda x: x.city == 'Neverland'))
    print(f'Total Person instances  {Persons.repository.total()}')
    print('Remove last instance added')
    Persons.repository.pop()
    print('Should be empty', Persons.repository.filter_by(lambda x: x.city == 'Neverland'))
    print(f'Total Person instances  {Persons.repository.total()}')

    print('Applying complex data filters and measure execution time..')
    filters = [
        lambda x: x.name.lower().endswith('s'),
        lambda x: x.name.lower().startswith('a'),
        lambda x: x.id in range(MIN, MAX),
        lambda x: x.id in range(MIN, MAX) or x.city.lower() in ('madrid', 'barcelona'),
        lambda x: len(x.city.split()) == 1,
        lambda x: len([i for i in list(x.name)]) == 5 and sum(range(0, x.id)) == 7,
    ]

    populate(Persons, get_person_data)
    apply_filters(Persons, filters)

    print('Can manage arbitrary models')
    Cats = Entity(name='Cat', attrs='age name city favourite_food')
    Cats.repository.add({'name': 'Garfield', 'age': 23, 'city': 'Neverland', 'favourite_food': 'Lasagna'})
    Cats.repository.add({'name': 'Mr. Whiskers', 'age': 6, 'city': 'London', 'favourite_food': 'Tuna'})
    Cats.repository.add({'name': 'Snowball', 'age': 4, 'city': 'Berlin', 'favourite_food': 'Potatos'})

    print('Is Garfield over here?', Cats.repository.filter_by(lambda cat: cat.name == 'Garfield'))
    print('Young cats', Cats.repository.filter_by(lambda cat: cat.age < 10))
