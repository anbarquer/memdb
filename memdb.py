# -*- coding: utf-8 -*-

import functools
import hashlib
from collections import namedtuple
from itertools import count
from time import time
from typing import List, Dict, Any, Callable, Optional, Iterator, Union


def measure(func):
    @functools.wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            print(f"Total execution time: {end_ if end_ > 0 else 0} ms")

    return _time_it


class Entity(object):
    _CACHE_SIZE = 512
    _HASH_ALG = 'sha256'
    _AUTO_KEY = True
    _PK_FIELD = 'id'
    _SIG_FIELD = 'signature'
    _ENCODING = 'utf-8'
    _START_COUNT = 1

    def _add(self, data: Dict) -> bool:
        new_values: Dict[str, Any] = {
            self._SIG_FIELD: self._get_signature(data),
        }

        new_values = {**new_values, **data}

        if self._AUTO_KEY:
            new_values.update({
                self._PK_FIELD: next(self._counter),
            })

        row: namedtuple = self._Model(**new_values)  # noqa

        if not self._find(row):  # noqa
            self._data.update({
                new_values.get(self._PK_FIELD) if self._AUTO_KEY else getattr(row, self._SIG_FIELD): row
            })

            return True
        return False

    def _find(self, data: Union[Dict, namedtuple]) -> bool:
        row: namedtuple = self._Model(**data) if isinstance(data, Dict) else data  # noqa

        return getattr(row, self._PK_FIELD) in self._data.keys() if self._AUTO_KEY \
            else getattr(row, self._SIG_FIELD) in self._data.keys()

    @functools.lru_cache(maxsize=_CACHE_SIZE)
    def _get_by_id(self, identifier: int) -> Optional[namedtuple]:
        try:
            return self._data.get(identifier)
        except AttributeError:
            return None

    def _get_all(self) -> List[namedtuple]:
        return [elem for _, elem in self._data.items()]

    def _remove_by_id(self, identifier: int) -> Optional[namedtuple]:
        try:
            return self._data.pop(identifier)
        except KeyError:
            return None

    def _remove_by(self, condition) -> None:
        self._data = {pk: elem for pk, elem in self._data.items() if not condition(elem)}

    def _total(self) -> int:
        return len(self._data.keys())

    def _pop(self) -> Optional[namedtuple]:
        try:
            *_, last = self._data.keys()
            return self._remove_by_id(last)
        except ValueError:
            return None

    @functools.lru_cache(maxsize=_CACHE_SIZE)
    def _filter_by(self, condition) -> List[namedtuple]:
        return list(filter(condition, self._get_all()))

    @functools.lru_cache(maxsize=_CACHE_SIZE)
    def _get_signature(self, data: Union[Dict, namedtuple]) -> str:
        row: namedtuple = self._Model(**data) if isinstance(data, Dict) else data

        content: bytes = ''.join([
            str(getattr(row, field))
            for field in self._Model._fields  # noqa
            if field.lower() not in (self._PK_FIELD, self._SIG_FIELD)
        ]).encode(self._ENCODING)

        hash_alg = hashlib.new(self._HASH_ALG)
        hash_alg.update(content)
        return hash_alg.hexdigest()

    def __init__(self,
                 model: str,
                 attrs: str,
                 autokey: bool = True,
                 cachesize: int = 512,
                 alg: str = 'sha256',
                 keyfield: str = 'id',
                 encoding: str = 'utf-8',
                 signature_field: str = 'signature',
                 start_count: int = 1) -> None:

        Entity._AUTO_KEY = autokey
        Entity._CACHE_SIZE = cachesize
        Entity._HASH_ALG = alg
        Entity._PK_FIELD = keyfield
        Entity._ENCODING = encoding
        Entity._SIG_FIELD = signature_field
        Entity._START_COUNT = start_count

        self._Model = namedtuple(model,
                                 f'{attrs} {Entity._SIG_FIELD}' if not autokey
                                 else f'{Entity._PK_FIELD} {attrs} {Entity._SIG_FIELD}')
        self._counter: Optional[Iterator] = count(Entity._START_COUNT)
        self._data: Dict = {}

        repository_methods: Dict[str, Callable] = {
            'add': lambda data: self._add(data),
            'get_by_id': lambda identifier: self._get_by_id(identifier),
            'get_all': lambda: self._get_all(),
            'remove_by_id': lambda identifier: self._remove_by_id(identifier),
            'remove_by': lambda identifier: self._remove_by(identifier),
            'total': lambda: self._total(),
            'pop': lambda: self._pop(),
            'filter_by': lambda condition: self._filter_by(condition),
            'find': lambda row: self._find(row),
        }

        self._repository = namedtuple(f'{self._Model.__name__}_Repository',
                                      ' '.join(repository_methods.keys()))(**repository_methods)  # noqa

    @property
    def repository(self):
        return self._repository
