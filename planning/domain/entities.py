"""Domain entities for the Planning context."""
class Thresholds:
    def __init__(self, humidity_min: float, temp_max: float):
        self.humidity_min = humidity_min
        self.temp_max = temp_max

class WateringDecision:
    def __init__(self, should_water: bool, duration_seconds: int):
        self.should_water = should_water
        self.duration_seconds = duration_seconds