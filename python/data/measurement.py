from dataclasses import dataclass
from datetime import datetime
from numbers import Number


@dataclass
class Measurement:
    name: str
    groups: dict
    value: Number
    time: datetime
