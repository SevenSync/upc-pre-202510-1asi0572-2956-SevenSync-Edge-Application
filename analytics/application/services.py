from analytics.domain.entities import PotRecord
from analytics.domain.services import PotRecordService, WateringCalculator
from analytics.infrastructure.repositories import PotRecordRepository
from iam.application.services import AuthApplicationService


class PotRecordApplicationService:
    def __init__(
            self,
            repo: PotRecordRepository,
            record_service: PotRecordService,
            threshold_service,
            auth_service: AuthApplicationService
    ):
        self.repo = repo
        self.record_service = record_service
        self.threshold_service = threshold_service
        self.auth_service = auth_service

    def create_pot_record(
            self,
            device_id: str,
            sensor_data: dict,
            created_at: str,
            api_key: str
    ) -> PotRecord:
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError("Dispositivo no autorizado")

        return self.repo.save(
            self.record_service.create_record(
                device_id=device_id,
                ph=sensor_data['ph'],
                humidity=sensor_data['humidity'],
                temperature=sensor_data['temperature'],
                salinity=sensor_data['salinity'],
                light=sensor_data['light'],
                created_at=created_at
            )
        )

    def get_last_record(self, device_id: str) -> PotRecord:
        return self.repo.get_last_record(device_id)

    def calculate_watering_time(
            self,
            device_id: str,
            sensor_data: dict,
            api_key: str
    ) -> int:
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError("Dispositivo no autorizado")

        thresholds = self.threshold_service.get_device_thresholds(device_id)

        return WateringCalculator.calculate(sensor_data, thresholds)