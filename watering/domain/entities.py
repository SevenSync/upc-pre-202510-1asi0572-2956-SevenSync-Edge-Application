from datetime import datetime

class WateringDecision:
    """Representa la decisión de riego tomada"""
    def __init__(self, device_id: str, decision: bool, reason: str, timestamp: datetime):
        self.device_id = device_id
        self.decision = decision  # True = regar, False = no regar
        self.reason = reason  # Explicación de la decisión
        self.timestamp = timestamp

class WateringExecution:
    """Representa la ejecución física del riego"""
    def __init__(self, device_id: str, duration: int, timestamp: datetime, success: bool = False):
        self.device_id = device_id
        self.duration = duration  # Segundos de riego
        self.timestamp = timestamp
        self.success = success