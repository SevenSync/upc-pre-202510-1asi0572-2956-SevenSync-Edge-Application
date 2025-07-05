"""
Database initialization for the MaceTech Edge Service.
"""
from peewee import SqliteDatabase

# Initialize SQLite database object
db = SqliteDatabase('macetech_edge.db')

def init_db_tables() -> None:
    """
    Creates all necessary tables. Assumes the database connection is already open.
    """
    # Esta función ya no maneja connect() o close()
    from iam.infrastructure.models import Device
    from analytics.infrastructure.models import PotRecord
    from watering.infrastructure.models import WateringLog

    db.create_tables([Device, PotRecord, WateringLog], safe=True)
    print("[DB] Tablas verificadas/creadas.")