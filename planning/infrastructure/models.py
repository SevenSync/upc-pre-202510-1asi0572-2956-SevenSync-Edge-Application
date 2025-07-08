from peewee import Model, AutoField, FloatField, ForeignKeyField
from shared.infrastructure.database import db
from iam.infrastructure.models import Device as DeviceModel

class PotThresholdModel(Model):
    id = AutoField()
    device = ForeignKeyField(DeviceModel, backref='thresholds', unique=True)
    temp_min = FloatField()
    temp_max = FloatField()
    humidity_min = FloatField()
    humidity_max = FloatField()
    light_min = FloatField()
    light_max = FloatField()
    salinity_min = FloatField()
    salinity_max = FloatField()
    ph_min = FloatField()
    ph_max = FloatField()

    class Meta:
        database = db
        table_name = 'pot_thresholds'