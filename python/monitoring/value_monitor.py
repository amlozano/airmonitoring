from abc import ABC
from numbers import Number


class ValueMonitor(ABC):

    def get_value(self) -> Number:
        pass
