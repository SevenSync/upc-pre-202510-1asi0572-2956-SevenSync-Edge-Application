"""Peewee models for the Pot Data context."""
from peewee import Model, AutoField, FloatField, IntegerField, CharField, DateTimeField
from shared.infrastructure.database import db

class PotRecord(Model):
    id = AutoField()
    device_id = CharField()
    temperature = FloatField()
    humidity = FloatField()
    light = IntegerField()
    salinity = FloatField()
    ph = FloatField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'pot_records'