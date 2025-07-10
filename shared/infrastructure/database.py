from peewee import SqliteDatabase

db = SqliteDatabase('macetech_edge.db')

def init_db_tables() -> None:
    from iam.infrastructure.models import Device
    # Import the model from the newly named 'arm' context
    from arm.infrastructure.models import PotStateRecordModel
    from watering.infrastructure.models import WateringExecutionModel
    from planning.infrastructure.models import PotThresholdModel

    db.create_tables([
        Device,
        PotStateRecordModel,
        WateringExecutionModel,
        PotThresholdModel
    ], safe=True)
    print("[DB] Tables verified/created.")