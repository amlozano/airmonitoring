# airmonitoring
Air monitoring setup to run on raspberry pi

## Requirements:

- docker
- docker-compose
- python 3

## Needed environment variables to run:

| Name              | Description             | 
| ----------------- | ----------------------- |
| INFLUXDB_USERNAME | InfluxDB admin username |
| INFLUXDB_PASSWORD | InfluxDB admin password |
| GRAFANA_USERNAME  | Grafana admin username  |
| GRAFANA_PASSWORD  | Grafana admin password  |

## Run with

```bash
./run.sh
```


