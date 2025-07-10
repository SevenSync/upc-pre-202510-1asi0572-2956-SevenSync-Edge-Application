from peewee import AutoField, FloatField, CharField, DateTimeField, BooleanField, Model, TextField
from shared.infrastructure.database import db

class WateringExecutionModel(Model):
    id = AutoField()
    device_id = CharField()
    duration_seconds = FloatField()
    timestamp = DateTimeField()
    success = BooleanField(default=False)
    reason = TextField() # ADDED: To store the detailed reason string.

    class Meta:
        database = db
        table_name = 'watering_executions'