from arm.domain.entities import PotStateRecord
from arm.domain.services import ArmService
from arm.infrastructure.repositories import PotStateRepository
from iam.application.services import AuthApplicationService


class ArmApplicationService:
    """
    # Application service for the ARM context. Orchestrates the flow
    # of creating and retrieving pot state records.
    """

    def __init__(self, repo: PotStateRepository, record_service: ArmService, auth_service: AuthApplicationService):
        self.repo = repo
        self.record_service = record_service
        self.auth_service = auth_service

    def create_state_record(self, device_id: str, api_key: str, **kwargs) -> PotStateRecord:
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError("Invalid device_id or API key.")

        record = self.record_service.create_state_record(device_id=device_id, **kwargs)
        return self.repo.save(record)

    def get_last_state_record(self, device_id: str, api_key: str) -> PotStateRecord | None:
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError("Invalid device_id or API key.")
        return self.repo.get_last_record(device_id)