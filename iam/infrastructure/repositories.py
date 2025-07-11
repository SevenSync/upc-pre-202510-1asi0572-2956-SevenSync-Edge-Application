# /iam/infrastructure/repositories.py
from datetime import datetime, timezone
from typing import Optional
import peewee
from iam.domain.entities import Device
from iam.infrastructure.models import Device as DeviceModel

class DeviceRepository:
    """
    # Repository for the IAM context. Manages persistence of Device entities.
    """
    @staticmethod
    def find_by_id_and_api_key(device_id: str, api_key: str) -> Optional[Device]:
        """
        # Finds a device only if both ID and API key match.
        """
        try:
            device_model = DeviceModel.get(
                (DeviceModel.device_id == device_id) & (DeviceModel.api_key == api_key)
            )
            return Device(device_model.device_id, device_model.api_key, device_model.created_at)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def find_by_id(device_id: str) -> Optional[Device]:
        """
        # Finds a device by its unique ID.
        """
        try:
            device_model = DeviceModel.get(DeviceModel.device_id == device_id)
            return Device(device_model.device_id, device_model.api_key, device_model.created_at)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_test_device() -> Device:
        """
        # Gets or creates the test device for development.
        # This refactored version is more robust and ensures the API key is always correct.
        """
        device_id = "1001"
        correct_api_key = "test-api-key-123"

        # Use get_or_create which is atomic and safe.
        device_model, created = DeviceModel.get_or_create(
            device_id=device_id,
            defaults={
                'api_key': correct_api_key,
                'created_at': datetime.now(timezone.utc)
            }
        )

        if created:
            print(f"DEBUG [Repository]: New test device '{device_id}' created in the database.")
        else:
            # If the device was not created, it already existed.
            # Let's ensure its API key is correct, fixing potential old/bad data.
            if device_model.api_key != correct_api_key:
                print(f"DEBUG [Repository]: Test device '{device_id}' existed with wrong API key. Updating it now.")
                device_model.api_key = correct_api_key
                device_model.save()
            else:
                print(f"DEBUG [Repository]: Test device '{device_id}' already exists and is correct.")

        # Return the domain entity based on the final state of the model.
        return Device(device_model.device_id, device_model.api_key, device_model.created_at)