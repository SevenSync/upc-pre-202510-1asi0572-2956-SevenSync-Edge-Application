"""
Peewee ORM model for pot records.

Defines the PotRecord database table structure for storing pot monitoring data.
"""
from peewee import Model, AutoField, FloatField, CharField, DateTimeField

from shared.infrastructure.database import db


class PotRecordModel(Model):
    """
    ORM model for the pot_records table.
    Represents a pot record entry in the database.
    """
    id = AutoField()
    device_id = CharField()
    ph = FloatField()
    humidity = FloatField()
    temperature = FloatField()
    salinity = FloatField()
    light = FloatField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'pot_records'