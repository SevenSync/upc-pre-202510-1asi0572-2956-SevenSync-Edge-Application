from planning.domain.entities import PotThreshold # The entity it provides
from shared.infrastructure.clients import CloudClient
from iam.application.services import AuthApplicationService

class PlanningApplicationService:
    """
    # The Application Service for the Planning context.
    # Its SOLE RESPONSIBILITY in this workflow is to provide the operational thresholds.
    # It abstracts away the fact that these thresholds come from the cloud.
    """
    def __init__(
        self,
        cloud_client: CloudClient,
        auth_service: AuthApplicationService
    ):
        self.cloud_client = cloud_client
        self.auth_service = auth_service
        # Note: The domain service would be needed if we had more complex planning logic here.
        # For now, this service is just a proxy to the cloud, which is a valid use case.

    def get_thresholds(self, device_id: str) -> PotThreshold | None:
        """
        # Provides the operational thresholds for a device.
        # This is its single, clear responsibility for the watering cycle.
        # The caller (WateringOrchestrator) doesn't know or care that these come from the cloud.
        """
        # Although the cloud endpoint is anonymous, we might want to add auth later.
        # For now, we don't need to use auth_service here, but it's good to have it available.
        return self.cloud_client.get_thresholds_for_device(device_id)