# app.py
from flask import Flask

from arm.interfaces.services import arm_api
from iam.interfaces.controllers import iam_api
# --- Infrastructure Imports ---
from shared.infrastructure.database import db, init_db_tables
from shared.infrastructure.clients import CloudClient

# --- Blueprint (Interface) Imports ---
from watering.interfaces.services import operation_api
from planning.interfaces.controllers import planning_api
from cloud_sync.interfaces.controllers import cloud_sync_api

# --- Application Service Imports ---
from iam.application.services import AuthApplicationService
from arm.application.services import ArmApplicationService
from planning.application.services import PlanningApplicationService
from watering.application.services import WateringOrchestrator
from cloud_sync.application.services import CloudSyncService

# --- Domain Service Imports ---
from arm.domain.services import ArmService
from planning.domain.services import PlanningService
from watering.domain.services import WateringExecutionService, WateringDecisionService

# --- Repository Imports ---
from arm.infrastructure.repositories import PotStateRepository
from watering.infrastructure.repositories import WateringRepository

# --- Placeholder for Hardware Interaction ---
class DeviceClient:
    """
    # This is a placeholder for the actual hardware client.
    # In a real implementation, this class would contain the logic
    # to interact with GPIO pins, MQTT, or other hardware interfaces.
    """
    def activate_watering(self, device_id: str, duration: float) -> bool:
        print(f"[DeviceClient] SIMULATING: Activating water pump for device '{device_id}' for {duration:.2f} seconds.")
        return True

# --- Flask App Initialization ---
app = Flask(__name__)

# =============================================================================
# --- COMPOSITION ROOT ---
# This is the ONLY place in the application where concrete classes are
# instantiated and wired together. This is the core of Dependency Injection.
# =============================================================================

# --- Infrastructure Instances ---
cloud_api_url = "https://macetech.azurewebsites.net"
cloud_client = CloudClient(cloud_api_url)
device_client = DeviceClient() # Instantiate our hardware client

# --- Repository Instances ---
auth_service = AuthApplicationService()
pot_state_repo = PotStateRepository()
watering_repo = WateringRepository()

# --- Domain Service Instances (they are stateless, so we only need one of each) ---
domain_arm_service = ArmService()
domain_planning_service = PlanningService()
watering_decision_service = WateringDecisionService()
watering_execution_service = WateringExecutionService()

# --- Application Service Instances (wiring everything together) ---

# ARM Service depends on its repository, domain service, and auth.
arm_app_service = ArmApplicationService(
    repo=pot_state_repo,
    record_service=domain_arm_service,
    auth_service=auth_service
)

# Planning Service depends on its domain service, the cloud client (for thresholds),
# the ARM service (for current state), and auth.
planning_app_service = PlanningApplicationService(
    planning_service=domain_planning_service,
    cloud_client=cloud_client,
    arm_service=arm_app_service,
    auth_service=auth_service
)

# Watering Orchestrator depends on the Planning service (to make decisions),
# a device client (to act), and its own repository (to log actions).
watering_orchestrator = WateringOrchestrator(
    planning_service=planning_app_service,
    device_client=device_client,
    repository=watering_repo
)

# Cloud Sync Service depends on the cloud client and the ARM service (to get data to sync).
cloud_sync_service = CloudSyncService(
    cloud_client=cloud_client,
    arm_service=arm_app_service
)


# --- Registering Services with Flask App ---
# We store the fully constructed services in the app's config,
# so the controllers can access them via `current_app`.
app.config["AUTH_APP_SERVICE"] = auth_service
app.config["ARM_APP_SERVICE"] = arm_app_service
app.config["PLANNING_APP_SERVICE"] = planning_app_service
app.config["WATERING_ORCHESTRATOR"] = watering_orchestrator
app.config["CLOUD_SYNC_SERVICE"] = cloud_sync_service

# =============================================================================
# --- BLUEPRINT REGISTRATION ---
# Connect the API controllers from each bounded context to the main app.
# =============================================================================
app.register_blueprint(iam_api)
app.register_blueprint(arm_api)
app.register_blueprint(operation_api)
app.register_blueprint(planning_api)
app.register_blueprint(cloud_sync_api)

# =============================================================================
# --- REQUEST HOOKS ---
# Manage the database connection lifecycle for each HTTP request.
# =============================================================================
@app.before_request
def before_request_handler():
    # Open the database connection before each request.
    if db.is_closed():
        db.connect()

@app.after_request
def after_request_handler(response):
    # Close the database connection after each request.
    if not db.is_closed():
        db.close()
    return response

# =============================================================================
# --- MAIN EXECUTION ---
# This block runs when the script is executed directly (e.g., `python app.py`).
# =============================================================================
if __name__ == "__main__":
    db.connect()
    init_db_tables()
    # Seed the database with a test device for development.
    auth_service.get_or_create_test_device()
    db.close()
    app.run(host='0.0.0.0', port=5000, debug=True)