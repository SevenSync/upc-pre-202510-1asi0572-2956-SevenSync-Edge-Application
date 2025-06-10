from datetime import datetime, timezone

from dateutil.parser import parse

from anaytics.domain.entities import PotRecord


class PotRecordService:
    """Service for managing pot records."""

    def __init__(self):
        """Initialize the PotServiceRecord."""

    @staticmethod
    def validate_record(device_id: str,
                        ph: float,
                        low_ph_threshold: float,
                        high_ph_threshold: float,
                        humidity: float,
                        low_humidity_threshold: float,
                        high_humidity_threshold: float,
                        temperature: float,
                        low_temperature_threshold: float,
                        high_temperature_threshold: float,
                        salinity: float,
                        low_salinity_threshold: float,
                        high_salinity_threshold: float,
                        light: float,
                        low_light_threshold: float,
                        high_light_threshold: float,):
        """Validate the pot record against thresholds."""
        if not (low_ph_threshold <= ph <= high_ph_threshold):
            raise ValueError("pH value is out of range")
        if not (low_humidity_threshold <= humidity <= high_humidity_threshold):
            raise ValueError("Humidity value is out of range")
        if not (low_temperature_threshold <= temperature <= high_temperature_threshold):
            raise ValueError("Temperature value is out of range")
        if not (low_salinity_threshold <= salinity <= high_salinity_threshold):
            raise ValueError("Salinity value is out of range")
        if not (low_light_threshold <= light <= high_light_threshold):
            raise ValueError("Light value is out of range")

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
        except (ValueError, TypeError):
            raise ValueError("Invalid data format")

        return PotRecord(device_id, ph, humidity, temperature, salinity, light, parsed_created_at)