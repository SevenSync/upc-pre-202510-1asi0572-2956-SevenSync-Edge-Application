"""Domain services for the Planning context."""
from analytics.domain.entities import PotRecord
from planning.domain.entities import Thresholds, WateringDecision


class PlanningService:
    @staticmethod
    def make_watering_decision(sensor_data: PotRecord, thresholds: Thresholds) -> WateringDecision:
        """
        Aplica las reglas de negocio para decidir si regar y por cuánto tiempo.
        """
        should_water = False
        if sensor_data.humidity < thresholds.humidity_min:
            should_water = True
        if sensor_data.temperature > thresholds.temp_max:
            should_water = True

        duration = 0
        if should_water:
            # Lógica de cálculo de duración (puede ser más compleja en el futuro)
            # Por ejemplo, regar más si la humedad es extremadamente baja.
            duration = 5  # Fijo en 5 segundos por ahora

        return WateringDecision(should_water=should_water, duration_seconds=duration)