from monitoring.sensors import Ccs811
from monitoring.value_monitor import ValueMonitor


class Ccs811Co2Monitor(ValueMonitor):
    _ccs811 = Ccs811.ccs811

    def get_value(self) -> int:
        if not self._ccs811.data_ready:
            raise RuntimeError("CCS811 sensor is not ready")
        return self._ccs811.eco2
