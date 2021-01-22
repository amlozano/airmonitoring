import time

from app.updater import Updater
from scheduling.scheduler import Scheduler


class TimeScheduler(Scheduler):

    def __init__(
            self,
            updater: Updater,
            periodicity_seconds: int):
        self._updater = updater
        self.periodicity_seconds = periodicity_seconds

    def start(self):
        while True:
            self._updater.update()
            time.sleep(self.periodicity_seconds)
