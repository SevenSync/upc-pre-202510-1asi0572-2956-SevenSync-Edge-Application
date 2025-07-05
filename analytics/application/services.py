from analytics.domain.entities import PotRecord
from analytics.domain.services import PotRecordService
from analytics.infrastructure.repositories import PotRecordRepository
from iam.application.services import AuthApplicationService
from planning.application.services import PlanningApplicationService


class PotRecordApplicationService:
    def __init__(self):
        self.repo = PotRecordRepository()
        self.record_service = PotRecordService()
        self.planning_service = PlanningApplicationService()
        self.auth_service = AuthApplicationService()

    def create_pot_record(
            self,
            device_id: str,
            temperature: float,
            humidity: float,
            light: float,
            salinity: float,
            ph: float,
            created_at: str,
            api_key: str
    ) -> PotRecord:
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError(f"Invalid device_id '{device_id}' or API key '{api_key}'.")

        record =self.record_service.create_record(device_id, temperature, humidity, light, salinity, ph, created_at)
        return self.repo.save(record)

    def get_records_by_device_id(
            self,
            device_id: str,
            api_key: str
    ) -> list[PotRecord]:
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError(f"Invalid device_id '{device_id}' or API key '{api_key}'.")

        return self.repo.get_records_by_device(device_id)

    def get_last_record( # Se necesita para el planning, especificamente "calculate_watering_time_from_tresholds"
            self,
            device_id: str,
            api_key: str
    ) -> PotRecord:
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError(f"Invalid device_id '{device_id}' or API key '{api_key}'.")

        return self.repo.get_last_record(device_id)

    def calculate_watering_time(
            self,
            device_id: str,
            api_key: str
    ) -> float:
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError(f"Invalid device_id '{device_id}' or API key '{api_key}'.")

        return  self.planning_service.calculate_watering_time_from_thresholds(device_id)
