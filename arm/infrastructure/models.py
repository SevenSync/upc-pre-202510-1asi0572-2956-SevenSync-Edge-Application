from peewee import Model, AutoField, FloatField, CharField, DateTimeField
from shared.infrastructure.database import db

class PotStateRecordModel(Model):
    """
    # Peewee ORM model for storing pot state records in the local SQLite database.
    """
    id = AutoField()
    device_id = CharField()
    temperature = FloatField()
    humidity = FloatField()
    light = FloatField()
    salinity = FloatField()
    ph = FloatField()
    battery_level = FloatField()
    water_level = FloatField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'pot_state_records'