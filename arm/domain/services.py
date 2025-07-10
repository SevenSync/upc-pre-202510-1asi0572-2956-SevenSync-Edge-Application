from datetime import datetime, timezone
from dateutil.parser import parse
from arm.domain.entities import PotStateRecord

class ArmService:
    """
    # Domain service for the ARM context. Contains pure business logic
    # related to validating and creating state records.
    """
    @staticmethod
    def create_state_record(device_id: str, created_at: str | None = None, **kwargs) -> PotStateRecord:
        """
        # Validates raw data and creates a PotStateRecord entity.
        """
        try:
            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format: {e}") from e

        return PotStateRecord(
            device_id=device_id,
            temperature=float(kwargs.get('temperature', 0)),
            humidity=float(kwargs.get('humidity', 0)),
            light=float(kwargs.get('light', 0)),
            salinity=float(kwargs.get('salinity', 0)),
            ph=float(kwargs.get('ph', 0)),
            battery_level=float(kwargs.get('battery_level', 100.0)),
            water_level=float(kwargs.get('water_level', 100.0)),
            created_at=parsed_created_at
        )