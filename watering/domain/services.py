"""Domain services for the Watering context."""
from analytics.domain.entities import PotRecord
from watering.domain.entities import Thresholds

class WateringDecisionService:
    @staticmethod
    def should_water(sensor_data: PotRecord, thresholds: Thresholds) -> bool:
        """Determines if watering is needed based on sensor data and thresholds."""
        if sensor_data.humidity < thresholds.humidity_min:
            return True
        if sensor_data.temperature > thresholds.temp_max:
            return True
        return False

    @staticmethod
    def calculate_duration(sensor_data: PotRecord, thresholds: Thresholds) -> int:
        """Calculates watering duration. Simple logic for now."""
        # A real implementation would have more complex logic here
        return 5 # Fixed 5 seconds for now