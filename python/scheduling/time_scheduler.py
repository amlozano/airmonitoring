import time
from datetime import datetime
from numbers import Number
from typing import List, Optional

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

    @staticmethod
    def _safe_read(named_monitor: NamedMonitor) -> Optional[Number]:
        try:
            return named_monitor.monitor.get_value()
        except RuntimeError as err:
            print(f"Error trying to read {named_monitor.metric_name}: {err}")
            return None

    @staticmethod
    def _safe_export(named_monitor: NamedMonitor, exporter: Exporter, current_time: datetime):
        value = TimeScheduler._safe_read(named_monitor)
        if value is not None:
            try:
                exporter.export_value(Measurement(named_monitor.metric_name, {}, value, current_time))
            except ConnectionError as err:
                print(f"Error trying to export values: {err}")

    def start(self):
        while True:
            current_time = self.current_time_provider.get_current_time()
            print("Updating measurements for time " + current_time.isoformat() + " ...")
            for named_monitor in self.monitors:
                self._safe_export(named_monitor, self.exporter, current_time)

            print("Measurements updated")
            time.sleep(self.periodicity_seconds)
