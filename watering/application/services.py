"""Application services for the Watering context (versión simplificada)."""
from datetime import datetime, timezone
import requests
from watering.domain.entities import WateringOperation
from watering.infrastructure.repositories import WateringLogRepository
from iam.application.services import AuthApplicationService

class WateringApplicationService:
    def __init__(self):
        self.log_repo = WateringLogRepository()
        self.iam_service = AuthApplicationService()

    def _get_decision_from_planning(self, device_id: str) -> dict:
        """Hace una llamada HTTP interna al endpoint de Planning para obtener la decisión."""
        planning_url = f"http://127.0.0.1:5000/api/v1/planning/devices/{device_id}/decision"
        try:
            response = requests.get(planning_url, timeout=2)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] No se pudo obtener la decisión desde Planning: {e}")
            return {"should_water": False, "duration_seconds": 0}

    def execute_and_log_operation(self, device_id: str, api_key: str) -> dict:
        """
        Obtiene la decisión de Planning, la registra y la devuelve.
        """
        if not self.iam_service.authenticate(device_id, api_key):
            raise PermissionError(f"Authentication failed for device '{device_id}'.")

        # 1. Obtener la decisión del Bounded Context de Planning
        decision = self._get_decision_from_planning(device_id)

        # 2. Crear y registrar la operación basada en la decisión recibida
        operation = WateringOperation(
            device_id=device_id,
            success=decision.get("should_water", False),
            duration=decision.get("duration_seconds", 0),
            timestamp=datetime.now(timezone.utc)
        )
        self.log_repo.save(operation)

        # 3. Devolver la decisión para que el firmware la ejecute
        return decision