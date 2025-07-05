"""Domain services for the Pot Data context."""
from datetime import datetime, timezone
from dateutil.parser import parse

from analytics.domain.entities import PotRecord


class PotRecordService:
    @staticmethod
    def create_record(device_id: str, sensor_data: dict, created_at: str | None) -> PotRecord:
        try:
            temp = float(sensor_data.get('temperature', 0))
            humidity = float(sensor_data.get('humidity', 0))

            if not (0 <= humidity <= 100):
                raise ValueError("Invalid Humidity value (must be 0-100)")

            parsed_created_at = datetime.now(timezone.utc) if not created_at else parse(created_at).astimezone(timezone.utc)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid data format: {e}")

        return PotRecord(
            device_id, temp, humidity,
            int(sensor_data.get('light', 0)),
            float(sensor_data.get('salinity', 0)),
            float(sensor_data.get('ph', 0)),
            parsed_created_at
        )