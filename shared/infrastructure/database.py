# /shared/infrastructure/database.py
from peewee import SqliteDatabase

db = SqliteDatabase('macetech_edge.db')

def init_db_tables() -> None:
    """
    # Initializes all database tables for all bounded contexts.
    # This function is called once at application startup.
    # It uses local imports to prevent circular dependency issues.
    """
    # Import all necessary models from their respective infrastructure layers.
    from iam.infrastructure.models import Device
    from arm.infrastructure.models import PotStateRecordModel
    from watering.infrastructure.models import WateringExecutionModel
    from planning.infrastructure.models import PotThresholdModel

    # Create all tables in a single, safe transaction.
    db.create_tables([
        Device,
        PotStateRecordModel,
        WateringExecutionModel,
        PotThresholdModel, # ADDED
    ], safe=True)
    print("[DB] Tables verified/created, including PotThresholds cache.")