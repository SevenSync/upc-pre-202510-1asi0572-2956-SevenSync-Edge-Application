from analytics.domain.entities import PotRecord
from analytics.infrastructure.models import PotRecordModel


class PotRecordRepository:
    @staticmethod
    def save(pot_record) -> PotRecord:
        record = PotRecordModel.create(
            device_id   =   pot_record.device_id,
            temperature =   pot_record.temperature,
            humidity    =   pot_record.humidity,
            light       =   pot_record.light,
            salinity    =   pot_record.salinity,
            ph          =   pot_record.ph,
            created_at  =   pot_record.created_at
        )
        return record

    @staticmethod
    def get_last_record(device_id: str) -> PotRecord:
        record_model = PotRecordModel.select().where(
            PotRecordModel.device_id == device_id
        ).order_by(PotRecordModel.created_at.desc()).first()

        if not record_model:
            raise ValueError(f"No records found for device {device_id}")

        return record_model

    @staticmethod
    def get_records_by_device(device_id: str) -> list[PotRecord]:
        query = PotRecordModel.select().where(
            (PotRecordModel.device_id == device_id)
        ).order_by(PotRecordModel.created_at.desc())

        return query