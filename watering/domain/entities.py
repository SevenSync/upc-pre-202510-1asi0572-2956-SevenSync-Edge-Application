"""Domain entities for the Watering context."""
from datetime import datetime

class WateringOperation:
    def __init__(self, device_id: str, success: bool, duration: int, timestamp: datetime, id: int = None):
        self.id = id
        self.device_id = device_id
        self.success = success
        self.duration = duration
        self.timestamp = timestamp

class Thresholds:
    def __init__(self, humidity_min: float, temp_max: float):
        self.humidity_min = humidity_min
        self.temp_max = temp_max