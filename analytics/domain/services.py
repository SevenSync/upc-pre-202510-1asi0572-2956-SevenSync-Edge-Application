from datetime import datetime, timezone, timedelta
from dateutil.parser import parse
from analytics.domain.entities import PotRecord


class PotRecordService:
    @staticmethod
    def create_record(device_id: str,
                      temperature: float,
                      humidity: float,
                      light: float,
                      salinity: float,
                      ph: float,
                      created_at: str) -> PotRecord:
        try:
            if not device_id:
                raise ValueError("Device ID cannot be empty, current value: {}".format(device_id))
            if not isinstance(temperature, (int, float)):
                raise ValueError("Temperature must be a number, current value: {}".format(temperature))
            if not isinstance(humidity, (int, float)):
                raise ValueError("Humidity must be a number, current value: {}".format(humidity))
            if not isinstance(light, (int, float)):
                raise ValueError("Light must be a number, current value: {}".format(light))
            if not isinstance(salinity, (int, float)):
                raise ValueError("Salinity must be a number, current value: {}".format(salinity))
            if not isinstance(ph, (int, float)):
                raise ValueError("ph must be a number, current value: {}".format(ph))

            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)

        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format: {str(e)}")

        return PotRecord(device_id, temperature, humidity, light, salinity, ph, parsed_created_at)