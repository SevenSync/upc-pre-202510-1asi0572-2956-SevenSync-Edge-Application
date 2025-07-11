# app.py
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from arm.interfaces.services import arm_api
from iam.domain.services import AuthService
from iam.infrastructure.repositories import DeviceRepository
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
from watering.domain.services import WateringDecisionService

# --- Repository Imports ---
from arm.infrastructure.repositories import PotStateRepository
from watering.infrastructure.repositories import WateringRepository


# --- Placeholder for Hardware Interaction ---
class DeviceClient:
    """
    # This is a placeholder for the actual hardware client.
    # In a real implementation, this class would interact with GPIO pins.
    """

    def activate_watering(self, device_id: str, duration: float) -> bool:
        print(f"[DeviceClient] SIMULATING: Activating water pump for device '{device_id}' for {duration:.2f} seconds.")
        return True


# --- Flask App Initialization ---
app = Flask(__name__)

# =============================================================================
# --- COMPOSITION ROOT ---
# This is the ONLY place where concrete classes are instantiated and wired together.
# =============================================================================

# --- Infrastructure Instances ---
cloud_api_url = "https://macetech.azurewebsites.net"
cloud_client = CloudClient(cloud_api_url)
device_client = DeviceClient()

# --- Repository Instances ---
device_repo = DeviceRepository()
pot_state_repo = PotStateRepository()
watering_repo = WateringRepository()

# --- Domain Service Instances (stateless) ---
domain_auth_service = AuthService() # <-- ADD
domain_arm_service = ArmService()
domain_planning_service = PlanningService()
watering_decision_service = WateringDecisionService()

# --- Application Service Instances (wiring everything together) ---

auth_service = AuthApplicationService(
    device_repository=device_repo,
    auth_service=domain_auth_service
)

arm_app_service = ArmApplicationService(
    repo=pot_state_repo,
    record_service=domain_arm_service,
    auth_service=auth_service
)

planning_app_service = PlanningApplicationService(
    cloud_client=cloud_client,
    auth_service=auth_service
)

# THIS IS THE CORRECTED BLOCK
watering_orchestrator = WateringOrchestrator(
    decision_service=watering_decision_service,
    planning_service=planning_app_service,
    arm_service=arm_app_service,
    auth_service=auth_service,
    device_client=device_client,
    repository=watering_repo,
    cloud_client=cloud_client
)

cloud_sync_service = CloudSyncService(
    cloud_client=cloud_client,
    arm_service=arm_app_service
)

# --- Registering Services with Flask App ---
app.config["AUTH_APP_SERVICE"] = auth_service
app.config["ARM_APP_SERVICE"] = arm_app_service
app.config["PLANNING_APP_SERVICE"] = planning_app_service
app.config["WATERING_ORCHESTRATOR"] = watering_orchestrator
app.config["CLOUD_SYNC_SERVICE"] = cloud_sync_service

# =============================================================================
# --- BLUEPRINT REGISTRATION ---
# =============================================================================
app.register_blueprint(iam_api)
app.register_blueprint(arm_api)
app.register_blueprint(operation_api)
app.register_blueprint(planning_api)
app.register_blueprint(cloud_sync_api)


# =============================================================================
# --- REQUEST HOOKS ---
# =============================================================================
@app.before_request
def before_request_handler():
    if db.is_closed():
        db.connect()


@app.after_request
def after_request_handler(response):
    if not db.is_closed():
        db.close()
    return response


# =============================================================================
# --- SCHEDULER FOR PERIODIC TASKS ---
# =============================================================================
def sync_state_job():
    with app.app_context():
        print("[Scheduler] Running scheduled job: sync_state_job")
        cloud_sync_service = app.config["CLOUD_SYNC_SERVICE"]
        auth_service = app.config["AUTH_APP_SERVICE"]

        device_id = "1001"
        api_key = auth_service.get_test_device_api_key()

        if api_key:
            cloud_sync_service.sync_latest_record_to_cloud(device_id, api_key)
        else:
            print("[Scheduler] Could not get API key for test device. Skipping sync.")


# =============================================================================
# --- MAIN EXECUTION ---
# =============================================================================
if __name__ == "__main__":
    db.connect()
    init_db_tables()
    auth_service.get_or_create_test_device()
    db.close()

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(sync_state_job, 'interval', minutes=15)
    scheduler.start()
    print("[Scheduler] Background job for state synchronization has been started.")

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)