# shared/infrastructure/clients.py
import requests

class AnalyticsClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_current_analytics(self, device_id: str, api_key: str) -> dict:
        url = f"{self.base_url}/device-status/{device_id}/records"
        headers = {"X-API-Key": api_key}
        response = requests.post(url, headers=headers, json={"device_id": device_id})
        response.raise_for_status()
        records = response.json().get("records", [])
        if not records:
            raise ValueError(f"No analytics records found for device {device_id}")
        return records[0]

class PlanningClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_thresholds(self, device_id: str, api_key: str) -> dict:
        url = f"{self.base_url}/thresholds/{device_id}"
        headers = {"X-API-Key": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

class DeviceClient:
    def activate_watering(self, device_id: str, duration: int) -> bool:
        print(f"[DEVICE CLIENT] Activating watering for device '{device_id}' for {duration} seconds.")
        return True