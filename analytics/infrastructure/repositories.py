from analytics.domain.entities import PotRecord
from analytics.infrastructure.models import PotRecordModel

class PotRecordRepository:

    @staticmethod
    def _to_entity(model: PotRecordModel) -> PotRecord:
        return PotRecord(
            id=model.id,
            device_id=model.device_id,
            temperature=model.temperature,
            humidity=model.humidity,
            light=model.light,
            salinity=model.salinity,
            ph=model.ph,
            created_at=model.created_at
        )

    @staticmethod
    def save(pot_record: PotRecord) -> PotRecord:
        record_model = PotRecordModel.create(
            device_id=pot_record.device_id,
            temperature=pot_record.temperature,
            humidity=pot_record.humidity,
            light=pot_record.light,
            salinity=pot_record.salinity,
            ph=pot_record.ph,
            created_at=pot_record.created_at
        )
        return PotRecordRepository._to_entity(record_model)

    @staticmethod
    def get_last_record(device_id: str) -> PotRecord | None:
        record_model = PotRecordModel.select().where(
            PotRecordModel.device_id == device_id
        ).order_by(PotRecordModel.created_at.desc()).first()

        if not record_model:
            return None

        return PotRecordRepository._to_entity(record_model)

    @staticmethod
    def get_records_by_device(device_id: str) -> list[PotRecord]:
        query = PotRecordModel.select().where(
            PotRecordModel.device_id == device_id
        ).order_by(PotRecordModel.created_at.desc())

        return [PotRecordRepository._to_entity(model) for model in query]