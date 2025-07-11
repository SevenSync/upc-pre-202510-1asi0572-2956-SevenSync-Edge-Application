# /watering/domain/services.py
from typing import NamedTuple
from arm.domain.entities import PotStateRecord
from planning.domain.entities import PotThreshold

class WateringAction(NamedTuple):
    """
    # A Value Object representing a calculated action.
    """
    should_water: bool
    volume_ml: float
    duration_seconds: float
    reason: str

class WateringDecisionService:
    """
    # This Domain Service contains the core, pure business logic for deciding IF and HOW to water.
    """
    VALVE_FLOW_RATE_LPS = 0.33  # Liters Per Second, based on typical hardware specs. This makes the service's calculations explicit and self-contained.


    @staticmethod
    def decide_action(state: PotStateRecord, thresholds: PotThreshold) -> WateringAction:
        """
        # Combines current device state and cloud-provided thresholds to decide on a course of action.
        """
        reasons_for_action = []

        if state.humidity < thresholds.humidity.min:
            reasons_for_action.append(f"Humidity ({state.humidity}%) is below minimum ({thresholds.humidity.min}%).")

        if state.temperature > thresholds.temperature.max:
            reasons_for_action.append(f"High temperature detected ({state.temperature}°C).")

        if not reasons_for_action:
            return WateringAction(should_water=False, volume_ml=0, duration_seconds=0, reason="Conditions are optimal.")

        # --- Calculate required VOLUME in milliliters ---
        volume_needed_ml = 0.0

        if state.humidity < thresholds.humidity.min:
            humidity_deficit = thresholds.humidity.min - state.humidity
            volume_needed_ml += humidity_deficit * 15.0

        if state.temperature > thresholds.temperature.max:
            volume_needed_ml += 50.0

        # --- Convert VOLUME to DURATION using the hardware CONSTANT ---
        flow_rate_ml_per_second = WateringDecisionService.VALVE_FLOW_RATE_LPS * 1000

        if flow_rate_ml_per_second <= 0:
            return WateringAction(should_water=False, volume_ml=0, duration_seconds=0, reason="Invalid flow rate constant (0).")

        calculated_duration = volume_needed_ml / flow_rate_ml_per_second
        final_duration = min(calculated_duration, 90.0)

        return WateringAction(
            should_water=True,
            volume_ml=round(volume_needed_ml, 2),
            duration_seconds=round(final_duration, 2),
            reason=" | ".join(reasons_for_action)
        )