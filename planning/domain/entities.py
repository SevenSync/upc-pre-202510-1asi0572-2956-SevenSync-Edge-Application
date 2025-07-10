from typing import NamedTuple

class Range(NamedTuple):
    """
    # A Value Object representing a numeric range with a minimum and maximum.
    # It's immutable and self-documenting.
    """
    min: float
    max: float

class PotThreshold:
    """
    # The Aggregate Root for the Planning context. It represents the complete
    # set of rules and operational parameters for a single device.
    # This entity is fetched from the cloud, not stored locally as a source of truth.
    """
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
    """
    # A Value Object that represents the output of the planning logic.
    # It's an immutable record of what the system decided and why.
    """
    def __init__(self, should_water: bool, duration_seconds: float = 0.0, reason: str = "N/A"):
        self.should_water = should_water
        self.duration_seconds = round(duration_seconds, 2)
        self.reason = reason