# -*- coding: utf-8 -*-

import functools
import hashlib
from collections import namedtuple
from itertools import count
from time import time
from typing import List, Dict, Any, Callable, Optional


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

    def _add(self, data: str) -> None:
        new: Dict[str, Any] = {'id': next(self._counter), **data}
        self._data.update({new.get('id'): self._Entity(**new)})  # noqa

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
    def _get_hash_key(self, instance: namedtuple) -> str:
        content: bytes = ''.join([
            str(getattr(instance, field))
            for field in self._Model._fields  # noqa
            if field.lower() != 'id'
        ]).encode('utf-8')

        hash_alg = hashlib.new(self._HASH_ALG)
        hash_alg.update(content)

        return hash_alg.hexdigest()

    def __init__(self,
                 model: str,
                 attrs: str,
                 autokey: bool = True,
                 cachesize: int = 512,
                 alg: str = 'sha256') -> None:

        Entity._AUTO_KEY = autokey
        Entity._CACHE_SIZE = cachesize
        Entity._HASH_ALG = alg

        self._Model = namedtuple(model, f'id {attrs}' if autokey else f'{attrs}')

        model_methods: Dict[str, Callable] = {
            'get_hash': self._get_hash_key(self._Model)
        }

        setattr(self._Model, 'get_hash', self._get_hash_key(self._Model))

        self._counter: Optional[Callable] = count(1) if autokey else None

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
            'get_hash': lambda instance: self._get_hash_key(instance),
        }

        self._repository = namedtuple(f'{self._Model.__name__}_Repository', ' '.join(repository_methods.keys()))
        self._repository(**repository_methods)

    @property
    def repository(self):
        return self._repository
