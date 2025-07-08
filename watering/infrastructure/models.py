from peewee import AutoField, FloatField, CharField, DateTimeField, BooleanField, Model

from shared.infrastructure.database import db

class WateringExecutionModel(Model):
    id = AutoField()
    device_id = CharField()
    duration = FloatField()
    timestamp = DateTimeField()
    success = BooleanField(default=False)

    class Meta:
        database = db
        table_name = 'watering_executions'