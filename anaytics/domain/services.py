from datetime import datetime, timezone, timedelta
from dateutil.parser import parse
from anaytics.domain.entities import PotRecord


class PotRecordService:
    """Service for managing pot records."""

    @staticmethod
    def create_record(device_id: str,
                      ph: float,
                      humidity: float,
                      temperature: float,
                      salinity: float,
                      light: float,
                      created_at: str | None) -> PotRecord:
        try:
            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format: {str(e)}")

        return PotRecord(device_id, ph, humidity, temperature, salinity, light, parsed_created_at)

class WateringCalculator:
    @staticmethod
    def calculate(sensor_data: dict, thresholds: dict) -> int:
        """Calcula tiempo de riego usando umbrales externos"""
        # 1. Obtener valores base de los umbrales
        base_time = thresholds.get('base_watering_seconds', 300)
        min_time = thresholds.get('min_watering_seconds', 60)
        max_time = thresholds.get('max_watering_seconds', 900)

        # 2. Factor de humedad
        humidity_threshold = thresholds.get('humidity_threshold', 30)
        humidity_factor = 1.0
        if sensor_data["humidity"] < humidity_threshold:
            humidity_factor = thresholds.get('humidity_factor', 1.3)

        # 3. Factor de temperatura
        temp = sensor_data["temperature"]
        temp_factor = 1.0
        if temp < thresholds.get('min_temp', 15):
            temp_factor = thresholds.get('cold_factor', 0.8)
        elif temp > thresholds.get('max_temp', 35):
            temp_factor = thresholds.get('heat_factor', 1.5)

        # 4. Cálculo final
        watering_time = base_time * humidity_factor * temp_factor
        return int(max(min_time, min(max_time, watering_time)))