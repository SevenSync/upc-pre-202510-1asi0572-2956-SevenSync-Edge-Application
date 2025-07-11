# /iam/application/services.py
from typing import Optional
from iam.domain.entities import Device
from iam.domain.services import AuthService
from iam.infrastructure.repositories import DeviceRepository


class AuthApplicationService:
    """
    # Application service for device authentication.
    # REFACTORED to use Dependency Injection.
    """

    # The constructor now explicitly requires its dependencies.
    def __init__(self, device_repository: DeviceRepository, auth_service: AuthService):
        self.device_repository = device_repository
        self.auth_service = auth_service

    def authenticate(self, device_id: str, api_key: str) -> bool:
        """
        # Authenticates a device by checking if a valid record exists.
        """
        print(f"DEBUG: Authenticating with -> deviceId: '{device_id}', apiKey: '{api_key}'")
        device: Optional[Device] = self.device_repository.find_by_id_and_api_key(device_id, api_key)
        print(f"DEBUG: Repository found device -> {device.__dict__ if device else 'None'}")
        return self.auth_service.authenticate(device)

    def get_or_create_test_device(self) -> Device:
        """
        # Gets or creates a test device for development.
        """
        return self.device_repository.get_or_create_test_device()

    def get_test_device_api_key(self) -> str | None:
        """
        # Helper method to retrieve the API key for the test device,
        # needed by the background scheduler job.
        """
        device = self.device_repository.find_by_id("smart-band-001")
        return device.api_key if device else None