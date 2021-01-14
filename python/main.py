import json
import os
import sys

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from data.named_monitor import NamedMonitor
from export.influx_exporter import InfluxExporter
from monitoring.dht11_humidity_monitor import Dht11HumidityMonitor
from monitoring.dht11_temperature_monitor import Dht11TemperatureMonitor
from monitoring.dht22_humidity_monitor import Dht22HumidityMonitor
from monitoring.dht22_temperature_monitor import Dht22TemperatureMonitor
from scheduling.current_time_provider import DatetimeCurrentTimeProvider
from scheduling.time_scheduler import TimeScheduler


def _get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


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

        monitors_config = config["monitors"]
        monitors = list(map(lambda mon: NamedMonitor(mon["name"], _get_class(mon["class"])()), monitors_config))

        scheduler = TimeScheduler(
            monitors,
            influx_exporter,
            config["timeGranularityInSeconds"],
            DatetimeCurrentTimeProvider())

        scheduler.start()


if __name__ == '__main__':
    main()
