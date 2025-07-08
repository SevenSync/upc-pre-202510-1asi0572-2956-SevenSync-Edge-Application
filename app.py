from flask import Flask

from shared.infrastructure.database import db, init_db_tables
from shared.infrastructure.clients import AnalyticsClient, PlanningClient, DeviceClient

from analytics.interfaces.services import analytics_api
from watering.interfaces.services import operation_api
from planning.interfaces.controllers import planning_api

from iam.application.services import AuthApplicationService
from analytics.application.services import PotRecordApplicationService
from planning.application.services import PlanningApplicationService
from watering.application.services import WateringOrchestrator

from analytics.domain.services import PotRecordService as DomainPotRecordService
from planning.domain.services import PlanningService as DomainPlanningService
from watering.domain.services import WateringExecutionService, WateringDecisionService

from analytics.infrastructure.repositories import PotRecordRepository
from watering.infrastructure.repositories import WateringRepository


app = Flask(__name__)

# --- Composition Root ---
auth_service = AuthApplicationService()
pot_record_repo = PotRecordRepository()
threshold_repo = ThresholdRepository()
watering_repo = WateringRepository()

domain_pot_record_service = DomainPotRecordService()
domain_planning_service = DomainPlanningService()
watering_decision_service = WateringDecisionService()
watering_execution_service = WateringExecutionService()

base_api_url = "http://127.0.0.1:5000/api/v1"
analytics_client = AnalyticsClient(base_api_url)
planning_client = PlanningClient(base_api_url)
device_client = DeviceClient()

analytics_app_service = PotRecordApplicationService(
    repo=pot_record_repo,
    record_service=domain_pot_record_service,
    auth_service=auth_service
)

planning_app_service = PlanningApplicationService(
    planning_service=domain_planning_service,
    threshold_repo=threshold_repo,
    analytics_service=analytics_app_service
)

watering_orchestrator = WateringOrchestrator(
    decision_service=watering_decision_service,
    execution_service=watering_execution_service,
    analytics_client=analytics_client,
    thresholds_client=planning_client,
    device_client=device_client,
    repository=watering_repo
)

app.config["AUTH_APP_SERVICE"] = auth_service
app.config["ANALYTICS_APP_SERVICE"] = analytics_app_service
app.config["PLANNING_APP_SERVICE"] = planning_app_service
app.config["WATERING_ORCHESTRATOR"] = watering_orchestrator

# --- Blueprint Registration ---
app.register_blueprint(analytics_api)
app.register_blueprint(operation_api)
app.register_blueprint(planning_api)

# --- Request Hooks ---

@app.before_request
def before_request_handler():
    db.connect(reuse_if_open=True)

@app.after_request
def after_request_handler(response):
    if not db.is_closed():
        db.close()
    return response

# --- Main Execution ---

if __name__ == "__main__":
    db.connect()
    init_db_tables()
    # Use the already instantiated auth_service for seeding
    auth_service.get_or_create_test_device()
    db.close()
    app.run(host='0.0.0.0', port=5000, debug=True)