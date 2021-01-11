import adafruit_dht
import board

from monitoring.value_monitor import ValueMonitor


class Dht11HumidityMonitor(ValueMonitor):
    _dhtDevice = adafruit_dht.DHT11(board.D4)

    def get_value(self) -> float:
        return self._dhtDevice.temperature
