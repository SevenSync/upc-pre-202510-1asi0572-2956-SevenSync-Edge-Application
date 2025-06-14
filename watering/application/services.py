from datetime import datetime

from watering.domain.entities import WateringExecution

from watering.domain.services import WateringDecisionService, WateringExecutionService


class WateringOrchestrator:
    """Orquestador principal de operaciones de riego"""

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
        # 1. Obtener datos analíticos actuales
        analytics = self.analytics_client.get_current_analytics(device_id)

        # 2. Obtener umbrales configurados
        thresholds = self.thresholds_client.get_thresholds(device_id)

        # 3. Tomar decisión de dominio
        decision = self.decision_service.make_watering_decision(analytics, thresholds)

        # 4. Calcular duración del riego
        duration = self.execution_service.calculate_water_duration(decision, analytics)

        # 5. Si no se debe regar, retornar ejecución vacía
        if duration <= 0:
            return WateringExecution(device_id, 0, datetime.now())

        # 6. Ejecutar riego físico
        execution_result = self.device_client.activate_watering(device_id, duration)

        # 7. Registrar ejecución
        execution = WateringExecution(
            device_id=device_id,
            duration=duration,
            timestamp=datetime.now()
        )
        execution.success = execution_result

        return self.repository.save(execution)
    # Commit message: