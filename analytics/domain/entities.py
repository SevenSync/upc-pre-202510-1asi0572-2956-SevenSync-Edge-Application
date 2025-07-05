"""Domain entities for the Pot Data context."""
from datetime import datetime

class PotRecord:
    def __init__(self, device_id: str, temp: float, humidity: float, light: int, salinity: float, ph: float, created_at: datetime, id: int = None):
        self.id = id
        self.device_id = device_id
        self.temperature = temp
        self.humidity = humidity
        self.light = light
        self.salinity = salinity
        self.ph = ph
        self.created_at = created_at