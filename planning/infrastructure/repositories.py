from peewee import DoesNotExist

from planning.domain.entities import PotThreshold, Range
from planning.infrastructure.models import PotThresholdModel


class ThresholdRepository:

    @staticmethod
    def _to_entity(model: PotThresholdModel) -> PotThreshold:
        return PotThreshold(
            id=model.id,
            device_id=model.device.device_id,
            temperature=Range(min=model.temp_min, max=model.temp_max),
            humidity=Range(min=model.humidity_min, max=model.humidity_max),
            light=Range(min=model.light_min, max=model.light_max),
            salinity=Range(min=model.salinity_min, max=model.salinity_max),
            ph=Range(min=model.ph_min, max=model.ph_max)
        )

    @staticmethod
    def get_for_device(device_id: str) -> PotThreshold | None:
        try:
            model = PotThresholdModel.get(PotThresholdModel.device == device_id)
            return ThresholdRepository._to_entity(model)
        except DoesNotExist:
            return None

    @staticmethod
    def save(threshold: PotThreshold) -> PotThreshold:
        model, created = PotThresholdModel.get_or_create(
            device=threshold.device_id,
            defaults={
                'temp_min': threshold.temperature.min,
                'temp_max': threshold.temperature.max,
                'humidity_min': threshold.humidity.min,
                'humidity_max': threshold.humidity.max,
                'light_min': threshold.light.min,
                'light_max': threshold.light.max,
                'salinity_min': threshold.salinity.min,
                'salinity_max': threshold.salinity.max,
                'ph_min': threshold.ph.min,
                'ph_max': threshold.ph.max
            }
        )
        if not created:
            model.temp_min = threshold.temperature.min
            model.temp_max = threshold.temperature.max
            model.humidity_min = threshold.humidity.min
            model.humidity_max = threshold.humidity.max
            model.light_min = threshold.light.min
            model.light_max = threshold.light.max
            model.salinity_min = threshold.salinity.min
            model.salinity_max = threshold.salinity.max
            model.ph_min = threshold.ph.min
            model.ph_max = threshold.ph.max
            model.save()

        return ThresholdRepository._to_entity(model)