# -*- coding: utf-8 -*-

import functools
from collections import namedtuple
from itertools import count

from typing import Any, Callable, Optional

DEFAULT_CACHE_SIZE: int = 512


class Config(object):
    def __init__(
            self,
            cache_size: int = DEFAULT_CACHE_SIZE
    ):
        self.cache_size = cache_size

    @cached_property
    def cache_size(self) -> int:



class Entity(object):

    def _add(self, data: str) -> None:
        new: dict[str | Any] = {'id': next(self._counter), **data}
        self._data.update({new.get('id'): self._Entity(**new)})  # noqa

    @functools.lru_cache(maxsize=_CACHE_SIZE)
    def _get_by_id(self, identifier: int) -> Optional[namedtuple]:
        try:
            return self._data.get(identifier)
        except AttributeError:
            return None

    def _get_all(self) -> list[namedtuple]:
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

    @functools.lru_cache(maxsize=self._config.cache_size)
    def _filter_by(self, condition) -> list[namedtuple]:
        return list(filter(condition, self._get_all()))

    def __init__(
            self,
            name: str,
            attrs: str,
            config: Config = None
    ) -> None:

        self._Entity = namedtuple(name, f'id {attrs}')
        self._counter = count(1)
        self._data: dict = {}

        methods: dict[str, Callable] = {
            'add': lambda data: self._add(data),
            'get_by_id': lambda identifier: self._get_by_id(identifier),
            'get_all': lambda: self._get_all(),
            'remove_by_id': lambda identifier: self._remove_by_id(identifier),
            'remove_by': lambda identifier: self._remove_by(identifier),
            'total': lambda: self._total(),
            'pop': lambda: self._pop(),
            'filter_by': lambda condition: self._filter_by(condition),
        }

        self._repository = namedtuple(f'{self._Entity.__name__}_Repository',
                                      ' '.join(methods.keys()))(**methods)  # noqa

        self._config = config if config is not None else Config()


    @property
    def repository(self):
        return self._repository
