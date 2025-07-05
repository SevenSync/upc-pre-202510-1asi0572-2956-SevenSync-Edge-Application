from typing import NamedTuple


class Range(NamedTuple):
    min: float
    max: float

class PotThreshold:
    def __init__(self,
                temperature: Range,
                humidity: Range,
                light: Range,
                salinity: Range,
                ph: Range,
                id: int = None):
        self.id = id
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.salinity = salinity
        self.ph = ph

class WateringDecision:
    def __init__(self, should_water: bool, duration_seconds: float = 0):
        self.should_water = should_water
        self.duration_seconds = duration_seconds