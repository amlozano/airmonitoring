from abc import ABC
from datetime import datetime


class CurrentTimeProvider(ABC):

    def get_current_time(self) -> datetime:
        pass


class DatetimeCurrentTimeProvider(CurrentTimeProvider):
    def get_current_time(self) -> datetime:
        return datetime.now()
