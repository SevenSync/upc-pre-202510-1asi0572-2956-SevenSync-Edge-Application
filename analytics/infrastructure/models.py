from peewee import Model, AutoField, FloatField, CharField, DateTimeField

from shared.infrastructure.database import db


class PotRecordModel(Model):
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