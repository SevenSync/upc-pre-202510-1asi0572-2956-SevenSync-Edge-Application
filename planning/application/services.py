"""Application services for the Planning context."""
from planning.domain.entities import WateringDecision

class PlanningApplicationService:
    def __init__(self):
        self.threshold_repo = None
        self.pot_record_repo = None
        self.planning_service = None

    def get_watering_decision(self, device_id: str) -> WateringDecision:
        """
        Orquesta el proceso para obtener una decisión de riego.
        """
        # 1. Obtener los datos más recientes de los sensores
        latest_record = self.pot_record_repo.get_last_record(device_id)

        # 2. Obtener los umbrales de configuración
        thresholds = self.threshold_repo.get_for_device(device_id)

        if not latest_record or not thresholds:
            # Si no tenemos datos, la decisión es no hacer nada
            return WateringDecision(should_water=False, duration_seconds=0)

        # 3. Llamar al servicio de dominio para que aplique la lógica
        return self.planning_service.make_watering_decision(latest_record, thresholds)