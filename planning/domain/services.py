from planning.domain.entities import PotThreshold, WateringDecision
from analytics.domain.entities import PotRecord

class PlanningService:

    @staticmethod
    def make_watering_decision(
        pot_record: PotRecord,
        thresholds: PotThreshold
    ) -> WateringDecision:

        if not pot_record:
            raise ValueError("PotRecord is required to make a decision.")
        if not thresholds:
            raise ValueError("PotThresholds are required to make a decision.")

        reasons_to_water = []
        if pot_record.humidity < thresholds.humidity.min:
            reasons_to_water.append(f"Humidity ({pot_record.humidity}%) is below minimum ({thresholds.humidity.min}%).")

        if pot_record.temperature > thresholds.temperature.max:
            reasons_to_water.append(f"Temperature ({pot_record.temperature}°C) is above maximum ({thresholds.temperature.max}°C).")

        if not reasons_to_water:
            return WateringDecision(should_water=False, reason="All metrics are within thresholds.")

        base_time = 30.0
        min_time = 10.0
        max_time = 90.0
        duration = base_time

        if pot_record.humidity < thresholds.humidity.min:
            humidity_diff = thresholds.humidity.min - pot_record.humidity
            duration += humidity_diff * 0.5

        if pot_record.temperature > thresholds.temperature.max:
            temp_diff = pot_record.temperature - thresholds.temperature.max
            duration += temp_diff * 1.0

        final_duration = max(min_time, min(max_time, duration))
        reason_summary = " | ".join(reasons_to_water)

        return WateringDecision(should_water=True, duration_seconds=final_duration, reason=reason_summary)