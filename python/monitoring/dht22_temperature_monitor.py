from monitoring.sensors import Dht22
from monitoring.value_monitor import ValueMonitor


class Dht22TemperatureMonitor(ValueMonitor):
    _dhtDevice = Dht22.dhtDevice

    def get_value(self) -> int:
        return self._dhtDevice.temperature
