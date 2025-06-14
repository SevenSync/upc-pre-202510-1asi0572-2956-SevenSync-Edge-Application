from typing import Optional
from iam.domain.entities import Device

class AuthService:
    def __init__(self):
        pass  # Placeholder implementation

    @staticmethod
    def authenticate(device: Optional[Device]) -> bool:
        return device is not None