from peewee import DoesNotExist
from arm.domain.entities import PotStateRecord
from arm.infrastructure.models import PotStateRecordModel

class PotStateRepository:
    """
    # Repository for the ARM context. Manages the persistence of PotStateRecord
    # entities, translating between the domain and the database model.
    """
    @staticmethod
    def _to_entity(model: PotStateRecordModel) -> PotStateRecord:
        return PotStateRecord(
            id=model.id,
            device_id=model.device_id,
            temperature=model.temperature,
            humidity=model.humidity,
            light=model.light,
            salinity=model.salinity,
            ph=model.ph,
            battery_level=model.battery_level,
            water_level=model.water_level,
            created_at=model.created_at
        )

    @staticmethod
    def save(record: PotStateRecord) -> PotStateRecord:
        model = PotStateRecordModel.create(
            device_id=record.device_id,
            temperature=record.temperature,
            humidity=record.humidity,
            light=record.light,
            salinity=record.salinity,
            ph=record.ph,
            battery_level=record.battery_level,
            water_level=record.water_level,
            created_at=record.created_at
        )
        return PotStateRepository._to_entity(model)

    @staticmethod
    def get_last_record(device_id: str) -> PotStateRecord | None:
        try:
            model = PotStateRecordModel.select().where(
                PotStateRecordModel.device_id == device_id
            ).order_by(PotStateRecordModel.created_at.desc()).get()
            return PotStateRepository._to_entity(model)
        except DoesNotExist:
            return None