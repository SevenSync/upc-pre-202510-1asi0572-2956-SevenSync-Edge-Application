"""Application services for the Pot Data context."""
from analytics.domain.entities import PotRecord
from analytics.domain.services import PotRecordService
from analytics.infrastructure.repositories import PotRecordRepository
from iam.application.services import AuthApplicationService

class PotRecordApplicationService:
    def __init__(self):
        self.repo = PotRecordRepository()
        self.service = PotRecordService()
        self.iam_service = AuthApplicationService()

    def create_pot_record(self, device_id: str, sensor_data: dict, created_at: str, api_key: str) -> PotRecord:
        if not self.iam_service.authenticate(device_id, api_key):
            raise PermissionError(f"Authentication failed for device '{device_id}'.")

        record = self.service.create_record(device_id, sensor_data, created_at)
        return self.repo.save(record)