"""Repositories for the Watering context."""
from watering.domain.entities import WateringOperation, Thresholds
from watering.infrastructure.models import WateringLog

class WateringLogRepository:
    @staticmethod
    def save(operation: WateringOperation) -> WateringOperation:
        log = WateringLog.create(
            device_id=operation.device_id,
            success=operation.success,
            duration=operation.duration,
            timestamp=operation.timestamp
        )
        operation.id = log.id
        return operation

class ThresholdRepository:
    @staticmethod
    def get_for_device(device_id: str) -> Thresholds:
        """
        Fetches thresholds. In a real system, this would make an HTTP GET request
        to the main cloud backend. For this edge app, we'll return fixed values.
        """
        # httpClient.begin("https://api.macetech.com/v1/devices/{device_id}/thresholds")
        # response = httpClient.GET() ...
        print(f"[Thresholds] Fetching for {device_id}. Returning mocked data.")
        return Thresholds(humidity_min=40.0, temp_max=30.0)