from datetime import datetime
from numbers import Number
from typing import Optional, List

from app.air_monitoring_app import AirMonitoringApp
from data.measurement import Measurement
from data.named_monitor import NamedMonitor
from export.exporter import Exporter
from monitoring.value_monitor import ValueMonitor
from scheduling.current_time_provider import CurrentTimeProvider


class TimeProviderStub(CurrentTimeProvider):

    def __init__(self, time: datetime):
        self._time = time

    def get_current_time(self) -> datetime:
        return self._time


class MonitorStub(ValueMonitor):

    def __init__(self, value, maybe_error: Optional[RuntimeError] = None):
        self._value = value
        self._error = maybe_error

    def get_value(self) -> Number:
        if self._error is not None:
            raise self._error
        return self._value


class ExporterSpy(Exporter):

    def __init__(self, maybe_error: Optional[RuntimeError]):
        self._error = maybe_error
        self._sent_measurements = []
        self._is_closed = False
        self._is_flushed = False

    def export_value(self, measurement: Measurement):
        if self._error is not None:
            raise self._error
        self._sent_measurements.append(measurement)

    def flush(self):
        self._is_flushed = True

    def close(self):
        self._is_closed = True

    def is_closed(self) -> bool:
        return self._is_closed

    def is_flushed(self) -> bool:
        return self._is_flushed

    def writen_content(self) -> List[Measurement]:
        return self._sent_measurements


def _fixture(
        metric_name: str = "",
        monitor_value: Number = 0,
        date: datetime = datetime(2021, 1, 23),
        write_error: Optional[RuntimeError] = None,
        read_error: Optional[RuntimeError] = None) -> (AirMonitoringApp, ExporterSpy):
    spy = ExporterSpy(write_error)
    time_provider = TimeProviderStub(date)
    app = AirMonitoringApp([NamedMonitor(metric_name, MonitorStub(monitor_value, read_error))], spy, time_provider)
    return app, spy


def test_it_should_export_the_measurement_read_from_monitor():
    metric_name = "testing"
    monitor_value = 53.4
    date = datetime(2021, 1, 10)

    (app, spy) = _fixture(metric_name=metric_name, monitor_value=monitor_value, date=date)
    app.update()

    assert spy.is_flushed() is True
    assert len(spy.writen_content()) == 1
    assert spy.writen_content()[0].time == date
    assert spy.writen_content()[0].name == metric_name
    assert spy.writen_content()[0].value == monitor_value
    assert spy.writen_content()[0].groups == {}


def test_it_should_be_silent_with_read_errors():
    (app, spy) = _fixture(read_error=RuntimeError("some message"))
    app.update()


def test_it_should_be_silent_with_write_errors():
    (app, spy) = _fixture(read_error=RuntimeError("some message"))
    app.update()


