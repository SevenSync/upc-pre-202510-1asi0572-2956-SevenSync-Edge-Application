from watering.domain.entities import WateringExecution
from watering.infrastructure.models import WateringExecutionModel

class WateringRepository:
    @staticmethod
    def _to_entity(model: WateringExecutionModel) -> WateringExecution:
        return WateringExecution(
            id=model.id,
            device_id=model.device_id,
            duration_seconds=model.duration_seconds,
            timestamp=model.timestamp,
            success=model.success,
            reason=model.reason # ADDED
        )

    @staticmethod
    def save(execution: WateringExecution) -> WateringExecution:
        record = WateringExecutionModel.create(
            device_id=execution.device_id,
            duration_seconds=execution.duration_seconds,
            timestamp=execution.timestamp,
            success=execution.success,
            reason=execution.reason # ADDED
        )
        return WateringRepository._to_entity(record)