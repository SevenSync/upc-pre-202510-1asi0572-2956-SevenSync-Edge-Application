from peewee import Model, AutoField, FloatField, CharField, DateTimeField

from shared.infrastructure.database import db


class PotRecordModel(Model):
    id = AutoField()
    device_id = CharField()
    temperature = FloatField()
    humidity = FloatField()
    light = FloatField()
    salinity = FloatField()
    ph = FloatField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'pot_records'