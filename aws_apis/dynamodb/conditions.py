from functools import reduce
from typing import Any, List, Union

from .utils import CONDITION_TYPE


class Condition:
    def __init__(
        self,
        operator: str,
        key: str = None,
        value: Any = None,
        condition: Union['Condition', List['Condition']] = None,
    ) -> None:
        self.operator = operator.lower()
        self.key = key
        self.value = value
        self.condition = condition

    @property
    def key_type(self):
        raise NotImplementedError

    def __call__(self):
        if self.operator == 'and':
            return reduce(lambda x, y: x() & y(), self.condition)
        elif self.operator == 'or':
            return reduce(lambda x, y: x() | y(), self.condition)
        elif self.operator == 'not':
            return ~ self.condition()
        else:
            _operator = getattr(self.key_type(self.key), self.operator)
            if isinstance(self.value, list) and self.operator == 'between':
                _min = min(self.value)
                _max = max(self.value)
                return _operator(_min, _max)
            elif self.value:
                return _operator(self.value)
            return _operator()


class AttrCondition(Condition):
    @property
    def key_type(self):
        return CONDITION_TYPE['Attr']


class KeyCondition(Condition):
    @property
    def key_type(self):
        return CONDITION_TYPE['Key']
