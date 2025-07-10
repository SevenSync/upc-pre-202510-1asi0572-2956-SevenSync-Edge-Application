from datetime import datetime, timezone
from watering.domain.entities import WateringExecution
from watering.domain.services import WateringDecisionService
from watering.infrastructure.repositories import WateringRepository
from planning.application.services import PlanningApplicationService
from arm.application.services import ArmApplicationService
from iam.application.services import AuthApplicationService

# Placeholder for the actual hardware client
class DeviceClient:
    def activate_watering(self, device_id: str, duration: float) -> bool:
        print(f"[DeviceClient] SIMULATING: Activating water pump for device '{device_id}' for {duration:.2f} seconds.")
        # In a real device, this would toggle a GPIO pin.
        return True

class WateringOrchestrator:
    """
    # The application service for the Watering context. It acts as the operational commander.
    # It orchestrates data gathering, decision making, physical action, and logging.
    """
    def __init__(self,
                 decision_service: WateringDecisionService,
                 planning_service: PlanningApplicationService,
                 arm_service: ArmApplicationService,
                 auth_service: AuthApplicationService,
                 device_client: DeviceClient,
                 repository: WateringRepository):
        self.decision_service = decision_service
        self.planning_service = planning_service
        self.arm_service = arm_service
        self.auth_service = auth_service
        self.device_client = device_client
        self.repository = repository

    def execute_watering_cycle(self, device_id: str, api_key: str) -> WateringExecution:
        """
        # Executes one full "sense -> think -> act -> log" cycle.
        """
        # 1. Sense: Gather all necessary information for the decision.
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError("Authentication failed for watering cycle.")

        current_state = self.arm_service.get_last_state_record(device_id, api_key)
        # The planning service encapsulates fetching thresholds from the cloud.
        thresholds = self.planning_service.cloud_client.get_thresholds_for_device(device_id)

        if not current_state or not thresholds:
            reason = "Missing local state data" if not current_state else "Missing thresholds from cloud"
            # Log a "non-action" for audit purposes and exit gracefully.
            return self.repository.save(WateringExecution(
                device_id=device_id, duration_seconds=0,
                timestamp=datetime.now(timezone.utc), success=False,
                reason=f"Cycle aborted: {reason}"
            ))

        # 2. Think: Delegate to the pure domain service to make a decision.
        action = self.decision_service.decide_action(current_state, thresholds)

        # 3. Act: If the decision is to water, perform the physical action.
        execution_success = False
        if action.should_water:
            execution_success = self.device_client.activate_watering(device_id, action.duration_seconds)

        # 4. Log: Create a record of the action (or non-action) and save it to the local DB.
        execution_log = WateringExecution(
            device_id=device_id,
            duration_seconds=action.duration_seconds if action.should_water else 0,
            timestamp=datetime.now(timezone.utc),
            success=execution_success,
            reason=action.reason
        )
        return self.repository.save(execution_log)