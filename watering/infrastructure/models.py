"""Peewee models for the Watering context."""
from peewee import Model, AutoField, CharField, BooleanField, IntegerField, DateTimeField
from shared.infrastructure.database import db

class WateringLog(Model):
    id = AutoField()
    device_id = CharField()
    success = BooleanField()
    duration = IntegerField()
    timestamp = DateTimeField()

    class Meta:
        database = db
        table_name = 'watering_logs'