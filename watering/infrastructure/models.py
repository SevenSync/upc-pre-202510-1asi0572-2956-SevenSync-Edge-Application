from peewee import Model, AutoField, FloatField, CharField, DateTimeField, BooleanField

from shared.infrastructure.database import db

class WateringExecutionModel:
    id = AutoField()
    device_id = CharField()
    duration = FloatField()
    timestamp = DateTimeField()
    success = BooleanField(default=False)

    class Meta:
        database = db
        table_name = 'watering_executions'