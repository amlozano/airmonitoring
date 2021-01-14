# airmonitoring
Air monitoring tool to run on raspberry pi.

It is composed of several modules that report data from different sensors to an InfluxDB database:

- Temperature and humidity sensor (DHT11). The code expects it to be placed at GPIO4
- Temperature and humidity sensor (DHT22). The code expects it to be placed at GPIO22 
- (not present yet) CO2 sensor

To work properly, these sensors should be added to the raspberry pi GPIO.
If you want to extend the functionality with other metrics, you need to create a child of [ValueMonitor](python/monitoring/value_monitor.py), see [TemperatureMonitor](python/monitoring/temperature_monitor.py) as example.
In the future, it will be able to add them as plug-in and configure them in the config.json

It runs three services in localhost:

| Service    | Port |
| ---------- | ---- |
| Grafana    | 3000 |
| InfluxDB   | 8083 |
| Chronograf | 8888 |

Grafana and Chronograf offer HTTP UIs that can be accessed with the browser.

## Requirements:

- docker
- docker-compose
- python 3
- [Adafruit blinka](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup)

## Needed environment variables to run:

| Name              | Description             | 
| ----------------- | ----------------------- |
| INFLUXDB_USERNAME | InfluxDB admin username |
| INFLUXDB_PASSWORD | InfluxDB admin password |
| GRAFANA_USERNAME  | Grafana admin username  |
| GRAFANA_PASSWORD  | Grafana admin password  |

They can be setup iside `~/.secrets/monitoring.sh`, (where the run command will look for them):

```bash
export INFLUXDB_USERNAME=blah
export INFLUXDB_PASSWORD=blah
export GRAFANA_USERNAME=blah
export GRAFANA_PASSWORD=blah
```

## Run with

```bash
./run_services.sh
./run_monitors.sh
```

## Future improvements
Added to Issues

