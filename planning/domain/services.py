from planning.domain.entities import PotThreshold, WateringDecision
from arm.domain.entities import PotStateRecord

class PlanningService:
    """
    # This is a pure, stateless Domain Service. Its only responsibility is to
    # contain the core business logic for making planning decisions.
    # It has no knowledge of infrastructure (databases, APIs).
    """
    @staticmethod
    def make_watering_decision(
        pot_record: PotStateRecord,
        thresholds: PotThreshold
    ) -> WateringDecision:
        """
        # Takes the current state (pot_record) and the rules (thresholds) to
        # produce a watering decision. This is a pure function.
        """
        if not pot_record:
            raise ValueError("PotStateRecord is required to make a decision.")
        if not thresholds:
            raise ValueError("PotThresholds are required to make a decision.")

        # --- 1. Decision Logic: Is there any reason to water? ---
        reasons_to_water = []
        if pot_record.humidity < thresholds.humidity.min:
            reasons_to_water.append(f"Humidity ({pot_record.humidity}%) is below minimum ({thresholds.humidity.min}%).")

        # More complex rules can be added here.
        if pot_record.temperature > thresholds.temperature.max:
            reasons_to_water.append(f"Temperature ({pot_record.temperature}°C) is above maximum ({thresholds.temperature.max}°C).")

        if not reasons_to_water:
            return WateringDecision(should_water=False, reason="All metrics are within thresholds.")

        # --- 2. Calculation Logic: If we water, for how long? ---
        base_time = 30.0  # Base watering time in seconds. Could be part of thresholds.
        min_time = 10.0
        max_time = 90.0
        duration = base_time

        # Adjust duration based on how severe the conditions are.
        if pot_record.humidity < thresholds.humidity.min:
            humidity_diff = thresholds.humidity.min - pot_record.humidity
            duration += humidity_diff * 0.5  # e.g., 0.5s extra per percentage point below min.

        if pot_record.temperature > thresholds.temperature.max:
            temp_diff = pot_record.temperature - thresholds.temperature.max
            duration += temp_diff * 1.0 # e.g., 1s extra per degree above max.

        # Ensure the final duration is within safe operational limits.
        final_duration = max(min_time, min(max_time, duration))
        reason_summary = " | ".join(reasons_to_water)

        return WateringDecision(should_water=True, duration_seconds=final_duration, reason=reason_summary)