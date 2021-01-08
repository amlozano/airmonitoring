from random import seed, gauss

from monitoring.value_monitor import ValueMonitor


class RandomTemperatureMonitor(ValueMonitor):
    seed(0)

    def get_value(self) -> float:
        return gauss(-20, 35)
