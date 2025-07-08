from planning.domain.services import PlanningService
from planning.domain.entities import WateringDecision
from planning.infrastructure.repositories import ThresholdRepository
from analytics.application.services import PotRecordApplicationService
from iam.application.services import AuthApplicationService

class PlanningApplicationService:
    def __init__(
        self,
        planning_service: PlanningService,
        threshold_repo: ThresholdRepository,
        analytics_service: PotRecordApplicationService,
        auth_service: AuthApplicationService
    ):
        self.planning_service = planning_service
        self.threshold_repo = threshold_repo
        self.analytics_service = analytics_service
        self.auth_service = auth_service

    def get_watering_decision(self, device_id: str, api_key: str) -> WateringDecision:
        if not self.auth_service.authenticate(device_id, api_key):
             raise PermissionError("Invalid device_id or API key.")

        latest_record = self.analytics_service.get_last_record(device_id, api_key)
        thresholds = self.threshold_repo.get_for_device(device_id)

        if not latest_record or not thresholds:
            reason = "Missing analytics data" if not latest_record else "Missing thresholds configuration"
            return WateringDecision(should_water=False, reason=reason)

        return self.planning_service.make_watering_decision(latest_record, thresholds)