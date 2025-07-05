"""Domain services for the Planning context."""



class PlanningService:
    @staticmethod
    def calculate_watering_time_from_thresholds(device_id: str) -> float:
        try:
            if not device_id:
                raise ValueError("Device ID cannot be empty, current value: {}".format(device_id))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format: {str(e)}")

class WateringCalculator:
    @staticmethod
    def calculate(device_id, thresholds: dict) -> float:
        base_time = float(thresholds.get('base_watering_seconds', 300))
        min_time = float(thresholds.get('min_watering_seconds', 60))
        max_time = float(thresholds.get('max_watering_seconds', 900))

        humidity_threshold = thresholds.get('humidity_threshold', 30)
        humidity_factor = 1.0
        if pot_record.humidity < humidity_threshold:
            humidity_factor = thresholds.get('humidity_factor', 1.3)

        temp = pot_record.temperature
        temp_factor = 1.0
        if temp < thresholds.get('min_temp', 15):
            temp_factor = thresholds.get('cold_factor', 0.8)
        elif temp > thresholds.get('max_temp', 35):
            temp_factor = thresholds.get('heat_factor', 1.5)

        watering_time = base_time * humidity_factor * temp_factor
        return max(min_time, min(max_time, watering_time))