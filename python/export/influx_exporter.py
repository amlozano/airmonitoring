from typing import List

from influxdb_client import Point

from data.measurement import Measurement
from export.exporter import Exporter
from export.write_api_proxy import WriteApiProxy


class ToInfluxPoint:

    @staticmethod
    def parse(measurement: Measurement) -> Point:
        point = Point(measurement.name)
        if measurement.groups is not None:
            for (key, value) in measurement.groups.items():
                point.tag(key, value)
        point.field("value", measurement.value).time(measurement.time)
        return point


class InfluxExporter(Exporter):

    def __init__(self, client: WriteApiProxy, database: str):
        self.client = client
        self.database = database

    def export_value(self, measurement: Measurement):
        bucket = f"{self.database}/1d"
        point = ToInfluxPoint.parse(measurement)
        print("Writing point: " + str(point.to_line_protocol()) + " to bucket " + bucket)
        self.client.write(bucket, point)
        self.client.flush()

    def close(self):
        self.client.flush()
        self.client.close()
