from datetime import datetime

class PotStateRecord:
    """
    # Represents a single, time-stamped snapshot of the pot's physical state.
    # This is the core domain entity for the ARM context.
    """
    def __init__(self,
                 device_id: str,
                 temperature: float,
                 humidity: float,
                 light: float,
                 salinity: float,
                 ph: float,
                 created_at: datetime,
                 battery_level: float = 100.0,
                 water_level: float = 100.0,
                 id: int = None):
        self.id = id
        self.device_id = device_id
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.salinity = salinity
        self.ph = ph
        self.created_at = created_at
        self.battery_level = battery_level
        self.water_level = water_level