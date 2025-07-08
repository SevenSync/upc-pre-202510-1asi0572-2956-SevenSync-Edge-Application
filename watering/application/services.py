from datetime import datetime

from watering.domain.entities import WateringExecution

from watering.domain.services import WateringDecisionService, WateringExecutionService


class WateringOrchestrator:

    def __init__(self,
                 decision_service: WateringDecisionService,
                 execution_service: WateringExecutionService,
                 analytics_client,
                 thresholds_client,
                 device_client,
                 repository):
        self.decision_service = decision_service
        self.execution_service = execution_service
        self.analytics_client = analytics_client
        self.thresholds_client = thresholds_client
        self.device_client = device_client
        self.repository = repository

    def execute_watering_workflow(self, device_id: str) -> WateringExecution:
        analytics = self.analytics_client.get_current_analytics(device_id)

        thresholds = self.thresholds_client.get_thresholds(device_id)

        decision = self.decision_service.make_watering_decision(analytics, thresholds)

        duration = self.execution_service.calculate_water_duration(decision, analytics)

        if duration <= 0:
            return WateringExecution(device_id, 0, datetime.now())

        execution_result = self.device_client.activate_watering(device_id, duration)

        execution = WateringExecution(
            device_id=device_id,
            duration=duration,
            timestamp=datetime.now()
        )
        execution.success = execution_result

        return self.repository.save(execution)