from abc import ABC

from data.measurement import Measurement


class Exporter(ABC):

    def export_value(self, measurement: Measurement):
        pass

    def flush(self):
        pass
