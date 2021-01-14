from typing import List

from influxdb_client import Point
from influxdb_client.client.write_api import WriteApi

from data.measurement import Measurement
from export.exporter import Exporter


class ToInfluxPoint:

    @staticmethod
    def parse(measurement: Measurement) -> Point:
        point = Point(measurement.name)
        for key in measurement.groups.keys():
            point.tag(key, measurement.groups[key])
        point.field("value", measurement.value)
        return point


class InfluxExporter(Exporter):
    _cache: List[Point] = []

    def __init__(self, client: WriteApi, database: str):
        self.client = client
        self.database = database

    def export_value(self, measurement: Measurement):
        bucket = f"{self.database}/1d"
        point = ToInfluxPoint.parse(measurement)
        print("Writing point: " + str(point.to_line_protocol()) + " to bucket " + bucket)
        self.client.write(bucket=bucket, record=point)
        self.client.close()

    def close(self):
        self.client.close()
