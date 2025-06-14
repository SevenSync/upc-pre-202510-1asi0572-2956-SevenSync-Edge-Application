from datetime import timedelta, datetime, timezone
from anaytics.domain.entities import PotRecord
from anaytics.infrastructure.models import PotRecordModel


class PotRecordRepository:
    @staticmethod
    def save(pot_record) -> PotRecord:
        record = PotRecordModel.create(
            device_id   =   pot_record.device_id,
            ph          =   pot_record.ph,
            humidity    =   pot_record.humidity,
            temperature =   pot_record.temperature,
            salinity    =   pot_record.salinity,
            light       =   pot_record.light,
            created_at  =   pot_record.created_at
        )
        return PotRecord(
            pot_record.device_id,
            pot_record.ph,
            pot_record.humidity,
            pot_record.temperature,
            pot_record.salinity,
            pot_record.light,
            pot_record.created_at,
            record.id
        )

    def get_last_record(self, device_id: str) -> PotRecord:
        """Obtener el último registro de un dispositivo"""
        # Consulta con Peewee
        record_model = PotRecordModel.select().where(
            PotRecordModel.device_id == device_id
        ).order_by(PotRecordModel.created_at.desc()).first()

        if not record_model:
            raise ValueError(f"No records found for device {device_id}")

        return PotRecord(
            device_id=record_model.device_id,
            ph=record_model.ph,
            humidity=record_model.humidity,
            temperature=record_model.temperature,
            salinity=record_model.salinity,
            light=record_model.light,
            created_at=record_model.created_at,
            id=record_model.id
        )

    @staticmethod
    def get_by_device(device_id: str, hours: int = 24) -> list[PotRecord]:
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=hours)

        query = PotRecordModel.select().where(
            (PotRecordModel.device_id == device_id) &
            (PotRecordModel.created_at >= time_threshold)
        ).order_by(PotRecordModel.created_at.desc())

        return [
            PotRecord(
                device_id=record.device_id,
                ph=record.ph,
                humidity=record.humidity,
                temperature=record.temperature,
                salinity=record.salinity,
                light=record.light,
                created_at=record.created_at,
                id=record.id
            )
            for record in query
        ]