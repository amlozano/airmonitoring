from abc import ABC
from typing import Any, Union, Iterable

from influxdb_client import WriteApi, Point


class WriteApiProxy(ABC):

    def write(self, bucket: str,
              record: Union[Point, Iterable[Point]]) -> Any:
        pass

    def flush(self):
        pass

    def close(self):
        pass


class InfluxWriteApiProxy(WriteApiProxy):

    def __init__(self, client: WriteApi):
        self._client = client

    def write(self, bucket: str,
              record: Union[Point, Iterable[Point]]) -> Any:
        self._client.write(bucket=bucket, record=record)

    def flush(self):
        self._client.flush()

    def close(self):
        self._client.flush()