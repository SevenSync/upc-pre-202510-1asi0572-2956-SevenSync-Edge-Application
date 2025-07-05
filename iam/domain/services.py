"""Domain services for the IAM bounded context."""
from typing import Optional
from iam.domain.entities import Device

class AuthService:
    @staticmethod
    def authenticate(device: Optional[Device]) -> bool:
        return device is not None