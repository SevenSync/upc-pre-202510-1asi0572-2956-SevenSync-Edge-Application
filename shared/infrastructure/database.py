from peewee import SqliteDatabase

db = SqliteDatabase('macetech_edge.db')

def init_db_tables() -> None:
    from iam.infrastructure.models import Device
    from analytics import PotRecord
    from watering.infrastructure.models import WateringLog

    db.create_tables([Device, PotRecord, WateringLog], safe=True)
    print("[DB] Tablas verificadas/creadas.")