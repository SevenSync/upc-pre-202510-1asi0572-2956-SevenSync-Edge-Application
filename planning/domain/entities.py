# planning/domain/entities.py
from typing import NamedTuple

class Range(NamedTuple):
    min: float
    max: float

class PotThreshold:
    def __init__(self,
                 device_id: str,
                 temperature: Range,
                 humidity: Range,
                 light: Range,
                 salinity: Range,
                 ph: Range,
                 id: int = None):
        self.id = id
        self.device_id = device_id
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.salinity = salinity
        self.ph = ph

class WateringDecision:
    def __init__(self, should_water: bool, duration_seconds: float = 0.0, reason: str = "N/A"):
        self.should_water = should_water
        self.duration_seconds = round(duration_seconds, 2)
        self.reason = reason