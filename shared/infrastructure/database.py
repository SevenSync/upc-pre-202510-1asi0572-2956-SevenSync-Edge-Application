from peewee import SqliteDatabase

db = SqliteDatabase('macetech_edge.db')

def init_db_tables() -> None:
    # IAM Model - Correcto
    from iam.infrastructure.models import Device
    # Analytics Model - Corregido para apuntar al modelo de Peewee
    from analytics.infrastructure.models import PotRecordModel
    # Watering Model - Asumiendo que se llama WateringLogModel o similar
    from watering.infrastructure.models import WateringExecutionModel # O como lo hayas llamado

    # La función create_tables ahora recibe las clases de modelo correctas
    db.create_tables([Device, PotRecordModel, WateringExecutionModel], safe=True)
    print("[DB] Tablas verificadas/creadas.")