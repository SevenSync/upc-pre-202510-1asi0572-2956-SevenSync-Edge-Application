# /planning/infrastructure/models.py
from peewee import Model, AutoField, FloatField, ForeignKeyField
from shared.infrastructure.database import db
from iam.infrastructure.models import Device as DeviceModel

class PotThresholdModel(Model):
    """
    # Peewee model to CACHE the thresholds fetched from the cloud.
    # This table allows the device to operate autonomously if it loses
    # internet connection by using the last known valid configuration.
    """
    id = AutoField()
    # Use a unique foreign key to ensure one set of thresholds per device.
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
        table_name = 'pot_thresholds_cache' # Name the table clearly as a cache.