import json
import os
import sys

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from data.named_monitor import NamedMonitor
from export.influx_exporter import InfluxExporter
from monitoring.temperature_monitor import RandomTemperatureMonitor
from scheduling.current_time_provider import DatetimeCurrentTimeProvider
from scheduling.time_scheduler import TimeScheduler


def main():
    config_location = 'default_config.json'
    if len(sys.argv) > 1:
        config_location = sys.argv[1]
    with open(config_location) as json_file:
        config = json.load(json_file)

        influx_config = config["influxDB"]

        influx_host = influx_config["hostname"]
        influx_port = influx_config["port"]
        influx_username = influx_config["username"]
        influx_password = os.environ[influx_config["passwordEnvName"]]
        influx_database = influx_config["database"]

        influx_client = InfluxDBClient(
            url=f'http://{influx_host}:{influx_port}',
            token=f'{influx_username}:{influx_password}',
            org='-')

        influx_exporter = InfluxExporter(influx_client.write_api(write_options=SYNCHRONOUS), influx_database)

        scheduler = TimeScheduler(
            [
                NamedMonitor("fake_temperature", RandomTemperatureMonitor())
            ],
            influx_exporter,
            config["timeGranularityInSeconds"],
            DatetimeCurrentTimeProvider())

        scheduler.start()


if __name__ == '__main__':
    main()
