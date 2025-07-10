from planning.domain.services import PlanningService
from planning.domain.entities import WateringDecision
from shared.infrastructure.clients import CloudClient
from arm.application.services import ArmApplicationService
from iam.application.services import AuthApplicationService

class PlanningApplicationService:
    """
    # The Application Service for the Planning context. It orchestrates the
    # workflow of making a watering decision by coordinating domain services
    # and infrastructure clients/repositories.
    """
    def __init__(
        self,
        planning_service: PlanningService,
        cloud_client: CloudClient,
        arm_service: ArmApplicationService,
        auth_service: AuthApplicationService
    ):
        self.planning_service = planning_service
        self.cloud_client = cloud_client
        self.arm_service = arm_service
        self.auth_service = auth_service

    def get_watering_decision(self, device_id: str, api_key: str) -> WateringDecision:
        """
        # Orchestrates the entire decision-making process.
        """
        # 1. Authorization
        if not self.auth_service.authenticate(device_id, api_key):
             raise PermissionError("Invalid device_id or API key.")

        # 2. Data Gathering
        # Get current state from the local ARM service.
        latest_record = self.arm_service.get_last_state_record(device_id, api_key)
        # Get rules from the cloud via the infrastructure client.
        thresholds = self.cloud_client.get_thresholds_for_device(device_id)

        # 3. Pre-condition check
        if not latest_record or not thresholds:
            reason = "Missing local state data" if not latest_record else "Could not fetch thresholds from cloud"
            return WateringDecision(should_water=False, reason=reason)

        # 4. Delegation to the Domain for the actual business logic
        return self.planning_service.make_watering_decision(latest_record, thresholds)