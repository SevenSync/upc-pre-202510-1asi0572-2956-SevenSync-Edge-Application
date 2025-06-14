# operation/domain/services.py
from datetime import datetime

from watering.domain.entities import WateringDecision


class WateringDecisionService:

    @staticmethod
    def make_watering_decision(analytics_data: dict, thresholds: dict) -> WateringDecision:
        # Lógica de decisión basada en múltiples factores
        reasons = []
        decision = False

        # Factor 1: Humedad por debajo del umbral
        if analytics_data["humidity"] < thresholds["min_humidity"]:
            decision = True
            reasons.append("humidity_below_threshold")

        # Factor 2: Temperatura por encima del umbral
        if analytics_data["temperature"] > thresholds["max_temperature"]:
            decision = True
            reasons.append("temperature_above_threshold")

        # Factor 3: Luz insuficiente (si aplica)
        if "min_light" in thresholds and analytics_data["light"] < thresholds["min_light"]:
            decision = True
            reasons.append("insufficient_light")

        return WateringDecision(
            device_id=analytics_data["device_id"],
            decision=decision,
            reason="|".join(reasons) if reasons else "no_need",
            timestamp=datetime.now()
        )


class WateringExecutionService:

    @staticmethod
    def calculate_water_duration(decision: WateringDecision, analytics: dict) -> int:
        if not decision.decision:
            return 0

        base_time = 2.5  # 2 minutos base
        humidity_factor = 1 - (analytics["humidity"] / 100)

        temp_factor = 1.0
        if analytics["temperature"] > 30:
            temp_factor = 1.5

        return int(base_time * humidity_factor * temp_factor)