from datetime import datetime

class WateringExecution:
    """
    # Represents a log of a watering action that was executed or considered.
    # This is the Aggregate Root for the Watering context. It's a historical record.
    """
    def __init__(self,
                 device_id: str,
                 duration_seconds: float,
                 timestamp: datetime,
                 success: bool,
                 reason: str,
                 id: int = None):
        self.id = id
        self.device_id = device_id
        self.duration_seconds = duration_seconds
        self.timestamp = timestamp
        self.success = success
        self.reason = reason