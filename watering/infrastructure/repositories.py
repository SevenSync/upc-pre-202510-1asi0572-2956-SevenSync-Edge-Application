# operation/infrastructure/repositories.py
from watering.domain.entities import WateringExecution
from watering.infrastructure.models import WateringExecutionModel


class WateringExecutionRepository:
    def save(self, execution: WateringExecution) -> WateringExecution:
        record = WateringExecutionModel.create(
            device_id=execution.device_id,
            duration=execution.duration,
            timestamp=execution.timestamp,
            success=execution.success
        )

        return WateringExecution(
            device_id=execution.device_id,
            duration=execution.duration,
            timestamp=execution.timestamp,
            success=record.success
        )