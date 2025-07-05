import uuid
from datetime import datetime

class PotRecord:

    def __init__(self,
                 device_id: str,
                 temperature: float,
                 humidity: float,
                 light: float,
                 salinity: float,
                 ph: float,
                 created_at: datetime,
                 id: int = None
                 ):
        self.id = id
        self.device_id = device_id
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.salinity = salinity
        self.ph = ph
        self.created_at = created_at