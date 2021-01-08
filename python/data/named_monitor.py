from dataclasses import dataclass

from monitoring.value_monitor import ValueMonitor


@dataclass
class NamedMonitor:
    metric_name: str
    monitor: ValueMonitor

