from planning.domain.entities import WateringDecision

class PlanningApplicationService:
    def __init__(self):
        self.threshold_repo = None
        self.pot_record_repo = None
        self.planning_service = None

    def get_watering_decision(self, device_id: str) -> WateringDecision:
        latest_record = self.pot_record_repo.get_last_record(device_id)
        thresholds = self.threshold_repo.get_for_device(device_id)

        if not latest_record or not thresholds:
            return WateringDecision(should_water=False, duration_seconds=0)

        return self.planning_service.make_watering_decision(latest_record, thresholds)