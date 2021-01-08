import logging
import time
from typing import List

from data.measurement import Measurement
from data.named_monitor import NamedMonitor
from export.exporter import Exporter
from scheduling.current_time_provider import CurrentTimeProvider
from scheduling.scheduler import Scheduler


class TimeScheduler(Scheduler):

    def __init__(
            self,
            monitors: List[NamedMonitor],
            exporter: Exporter,
            periodicity_seconds: int,
            current_time_provider: CurrentTimeProvider):
        self.monitors = monitors
        self.exporter = exporter
        self.periodicity_seconds = periodicity_seconds
        self.current_time_provider = current_time_provider

    def start(self):
        while True:
            current_time = self.current_time_provider.get_current_time()
            logging.info("Updating measurements for time " + current_time.isoformat() + " ...")
            for named_monitor in self.monitors:
                value = named_monitor.monitor.get_value()
                try:
                    self.exporter.export_value(
                        Measurement(named_monitor.metric_name, {}, value, current_time))
                except ConnectionError as err:
                    logging.error("Error trying to export values: {0}".format(err))

            logging.info("Measurements updated")
            time.sleep(self.periodicity_seconds)
