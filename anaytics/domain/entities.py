"""Domain entities for the Health-bounded context."""
from datetime import datetime


class PotRecord:
    """Includes all sensor data from an specific pot.

    Attributes:
        id (int, optional): Unique identifier for the record.
        device_id (str): Identifier of the device that generated the record.
        ph (float): pH level of the pot.
        humidity (float): Humidity level of the pot.
        temperature (float): Temperature of the pot.
        salinity (float): Salinity level of the pot.
        light (float): Light intensity in the pot.
        created_at (datetime): Timestamp when the record was created.
    """

    def __init__(self, device_id: str,
                 ph: float,
                 humidity: float,
                 temperature: float,
                 salinity: float,
                 light: float,
                 created_at: datetime,
                 id: int = None):

        self.id = id
        self.device_id = device_id
        self.ph = ph
        self.humidity = humidity
        self.temperature = temperature
        self.salinity = salinity
        self.light = light
        self.created_at = created_at
