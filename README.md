# memdb
In memory key/value database in pure Python

```
 $ python3 example.py 

    Filter using Python lambda functions [Person(id=1, name='This is a test', age=23, city='Neverland')]
    Total Person instances  1
    Remove last instance added
    Should be empty []
    Total Person instances  0
    Applying complex data filters and measure execution time..
    Loading 40362 instances
    Total execution time: 204 ms
    Applying 43146 filters
    Total execution time: 1184 ms
    Can manage arbitrary models
    Is Garfield over here? [Cat(id=1, age=23, name='Garfield', city='Neverland', favourite_food='Lasagna')]
    Young cats [Cat(id=2, age=6, name='Mr. Whiskers', city='London', favourite_food='Tuna'), Cat(id=3, age=4, name='Snowball', city='Berlin', favourite_food='Potatos')]

```