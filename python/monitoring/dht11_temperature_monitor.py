from monitoring.dht11 import Dht11
from monitoring.value_monitor import ValueMonitor


class Dht11TemperatureMonitor(ValueMonitor):
    _dhtDevice = Dht11.dhtDevice

    def get_value(self) -> float:
        return self._dhtDevice.temperature
