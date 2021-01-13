from monitoring.value_monitor import ValueMonitor
import mh_z19


class Mhz19Co2Monitor(ValueMonitor):

    def get_value(self) -> int:
        return mh_z19.read()['co2']
