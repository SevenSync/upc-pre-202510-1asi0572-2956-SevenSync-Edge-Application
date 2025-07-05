"""Repositories for the Pot Data context."""
from analytics.domain.entities import PotRecord
from analytics.infrastructure.models import PotRecord as PotRecordModel

class PotRecordRepository:
    @staticmethod
    def save(pot_record: PotRecord) -> PotRecord:
        record = PotRecordModel.create(
            device_id=pot_record.device_id,
            temperature=pot_record.temperature,
            humidity=pot_record.humidity,
            light=pot_record.light,
            salinity=pot_record.salinity,
            ph=pot_record.ph,
            created_at=pot_record.created_at
        )
        pot_record.id = record.id
        return pot_record

    @staticmethod
    def get_last_record(device_id: str) -> PotRecord:
        model = PotRecordModel.select().where(PotRecordModel.device_id == device_id).order_by(PotRecordModel.created_at.desc()).get()
        return PotRecord(
            model.device_id, model.temperature, model.humidity, model.light,
            model.salinity, model.ph, model.created_at, model.id
        )