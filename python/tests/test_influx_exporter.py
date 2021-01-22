from datetime import datetime
from numbers import Number
from typing import Dict, Iterable, Any, Optional, Union

import pytest
from influxdb_client import Point

from data.measurement import Measurement
from export.influx_exporter import InfluxExporter
from export.write_api_proxy import WriteApiProxy


class WriteApiSpy(WriteApiProxy):

    def __init__(self, maybe_error: Optional[RuntimeError]):
        self._error = maybe_error
        self._sent_measurements = {}
        self._is_closed = False
        self._is_flushed = False

    def write(self, bucket: str,
              record: Union[Point, Iterable[Point]]) -> Any:
        if self._error is not None:
            raise self._error
        self._sent_measurements[bucket] = record

    def close(self):
        self._is_closed = True

    def flush(self):
        self._is_flushed = True

    def is_closed(self) -> bool:
        return self._is_closed

    def is_flushed(self) -> bool:
        return self._is_flushed

    def writen_content(self) -> Dict:
        return self._sent_measurements


def _fixture(name: str = "", groups: Dict[str, str] = None, value: Number = 0, date: datetime = datetime(2021, 1, 14),
             maybe_error: Optional[RuntimeError] = None) -> (InfluxExporter, WriteApiSpy, Measurement):
    spy = WriteApiSpy(maybe_error)
    exporter = InfluxExporter(spy, "test")
    return exporter, spy, Measurement(name, groups, value, date)


def test_it_should_export_a_single_measurement_to_influx():
    name = "testing"
    group_key = "test_key"
    group_value = "test_value"
    value = 53.4
    date = datetime(2021, 1, 14)

    (influx_exporter, api_spy, measurement) = _fixture(name, {group_key: group_value}, value, date)
    influx_exporter.export_value(measurement)

    assert api_spy.is_flushed() is True
    assert api_spy.writen_content()["test/1d"].to_line_protocol() == \
           Point(name).tag(group_key, group_value).field("value", value).time(date).to_line_protocol()


def test_it_should_export_a_single_measurement_without_groups_to_influx():
    name = "testing"
    value = 53.4
    groups = None
    date = datetime(2021, 1, 14)

    (influx_exporter, api_spy, measurement) = _fixture(name=name, groups=groups, value=value, date=date)
    influx_exporter.export_value(measurement)

    assert api_spy.is_flushed() is True
    assert api_spy.writen_content()["test/1d"].to_line_protocol() == \
           Point(name).field("value", value).time(date).to_line_protocol()


def test_it_should_raise_an_error_when_client_fails():
    (influx_exporter, api_spy, measurement) = _fixture(maybe_error=RuntimeError("some message"))
    with pytest.raises(RuntimeError) as err:
        influx_exporter.export_value(measurement)

    assert "some message" in str(err.value)


def test_it_should_flush_and_close_client_when_close():
    (influx_exporter, api_spy, measurement) = _fixture()
    influx_exporter.close()

    assert api_spy.is_flushed() is True
    assert api_spy.is_closed() is True
