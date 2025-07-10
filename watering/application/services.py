# /watering/application/services.py
from datetime import datetime, timezone
from watering.domain.entities import WateringExecution
from watering.domain.services import WateringDecisionService
from watering.infrastructure.repositories import WateringRepository
from planning.application.services import PlanningApplicationService
from arm.application.services import ArmApplicationService
from iam.application.services import AuthApplicationService
from shared.infrastructure.clients import CloudClient


# --- Placeholder for Hardware Interaction ---
class DeviceClient:
    @staticmethod
    def activate_watering(device_id: str, duration: float) -> bool:
        print(f"[DeviceClient] SIMULATING: Activating water pump for device '{device_id}' for {duration:.2f} seconds.")
        return True


# --- The Main Orchestrator Class ---
class WateringOrchestrator:
    """
    # The application service for the Watering context. It acts as the operational commander.
    # It orchestrates data gathering, decision-making, physical action, and logging.
    """

    def __init__(self,
                 decision_service: WateringDecisionService,
                 planning_service: PlanningApplicationService,
                 arm_service: ArmApplicationService,
                 auth_service: AuthApplicationService,
                 device_client: DeviceClient,
                 repository: WateringRepository,
                 cloud_client: CloudClient):
        self.decision_service = decision_service
        self.planning_service = planning_service
        self.arm_service = arm_service
        self.auth_service = auth_service
        self.device_client = device_client
        self.repository = repository
        self.cloud_client = cloud_client

    def execute_watering_cycle(self, device_id: str, api_key: str) -> WateringExecution:
        """
        # Executes one full "sense -> think -> act -> log -> sync" cycle.
        # This refactored version uses a guard clause for clarity and correctness.
        """
        # --- 1. Sense: Gather all necessary information ---
        if not self.auth_service.authenticate(device_id, api_key):
            raise PermissionError("Authentication failed for watering cycle.")

        current_state = self.arm_service.get_last_state_record(device_id, api_key)
        thresholds = self.planning_service.get_thresholds(device_id)

        # --- 2. Guard Clause: Handle failure cases first and exit early ---
        if not current_state or not thresholds:
            # Determine the specific reason for failure.
            reason = "Missing local state data" if not current_state else "Missing thresholds from cloud"

            # Create a log entry for the aborted cycle for debugging purposes.
            aborted_log = WateringExecution(
                device_id=device_id,
                duration_seconds=0,
                timestamp=datetime.now(timezone.utc),
                success=False,
                reason=f"Cycle aborted: {reason}"
            )
            # Save the failure log locally...
            saved_log = self.repository.save(aborted_log)
            # ...and try to sync it to the cloud so we are aware of the problem.
            self.cloud_client.push_watering_log(saved_log)
            # Exit the function immediately.
            return saved_log

        # --- "Happy Path" continues here, un-nested and clean ---

        # --- 3. Think: Delegate to the pure domain service to make a decision ---
        # This is now only called ONCE, in the success case.
        action = self.decision_service.decide_action(current_state, thresholds)

        # --- 4. Act: Perform the physical action if needed ---
        execution_success = False
        if action.should_water:
            execution_success = self.device_client.activate_watering(device_id, action.duration_seconds)

        # --- 5. Log Locally: Create a record of the action (or non-action) ---
        execution_log = WateringExecution(
            device_id=device_id,
            duration_seconds=action.duration_seconds,  # Will be 0 if should_water is False
            timestamp=datetime.now(timezone.utc),
            success=execution_success,
            reason=action.reason
        )
        saved_log = self.repository.save(execution_log)

        # --- 6. Sync Log to Cloud ---
        print(f"[Orchestrator] Attempting to sync watering log to cloud for device {device_id}...")
        sync_success = self.cloud_client.push_watering_log(saved_log)
        if sync_success:
            print("[Orchestrator] Log sync successful.")
        else:
            print("[Orchestrator] WARNING: Log sync to cloud failed. The log is saved locally.")

        return saved_log