from typing import Optional

import peewee

from iam.domain.entities import Device
from iam.infrastructure.models import Device as DeviceModel

class DeviceRepository:

    @staticmethod
    def find_by_id_and_api_key(device_id: str, api_key: str) -> Optional[Device]:
        try:
            device = DeviceModel.get(
                (DeviceModel.device_id == device_id) & (DeviceModel.api_key == api_key)
            )
            return Device(device.device_id, device.api_key, device.created_at)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_test_device() -> Device:
        device, _ = DeviceModel.get_or_create(
            device_id="smart-band-001",
            defaults={"api_key": "test-api-key-123", "created_at": "2025-06-04T23:23:00Z"}
        )
        return Device(device.device_id, device.api_key, device.created_at)