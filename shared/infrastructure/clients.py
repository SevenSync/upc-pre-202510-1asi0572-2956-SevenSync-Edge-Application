# /shared/infrastructure/clients.py
import requests

from planning.domain.entities import PotThreshold, Range
from arm.domain.entities import PotStateRecord
from watering.domain.entities import WateringExecution


class CloudClient:
    """
    # An infrastructure client responsible for all communication
    # with the MaceTech Cloud API. It acts as an Anti-Corruption Layer.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    # --- Watering Log Synchronization (This is the method to refactor) ---

    def push_watering_log(self, execution_log: WateringExecution) -> bool:
        """
        # Pushes a watering execution log to the new cloud endpoint.
        # This aligns with the final WateringController in the C# backend.
        """
        # UPDATED: The URL now points to the new route structure.
        url = f"{self.base_url}/api/v1/watering-history/device/{execution_log.device_id}/create-log"

        # The payload matches the CreateWateringLogResource record in C#.
        payload = {
            "durationSeconds": execution_log.duration_seconds,
            "wasSuccessful": execution_log.success,
            "reason": execution_log.reason
        }

        try:
            print(f"[CloudClient] Pushing watering log to: {url}")
            # This endpoint is [AllowAnonymous], so no Authorization header is needed.
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            # The backend now returns the created resource, so a 2xx status is enough for success.
            return response.ok
        except requests.exceptions.RequestException as e:
            print(f"[CloudClient] ERROR: Could not push watering log. Details: {e}")
            return False

    # --- Pot Provisioning Methods (Used for testing and simulation) ---

    def create_pot_in_cloud(self) -> str | None:
        """
        # Simulates the manufacturing step. Creates a new pot in the cloud's ARM context.
        # This corresponds to the `POST /api/v1/Pots` endpoint.
        # Returns the new Pot ID if successful, otherwise None.
        """
        url = f"{self.base_url}/api/v1/Pots"
        try:
            print(f"[CloudClient] Creating pot at: {url}")
            response = requests.post(url, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP error codes (4xx or 5xx)
            # The C# controller returns a { "id": "value" } object
            return str(response.json()["id"])
        except requests.exceptions.RequestException as e:
            print(f"[CloudClient] ERROR: Could not create pot in cloud. Details: {e}")
            return None

    def assign_pot_to_user(self, pot_id: str, user_token: str, name: str, location: str) -> bool:
        """
        # Simulates a user assigning the pot to their account via a mobile app.
        # This corresponds to `PUT /api/v1/Pots/{potId}/assignee`.
        """
        url = f"{self.base_url}/api/v1/Pots/{pot_id}/assignee"
        headers = {"Authorization": user_token} # Assuming the token includes "Bearer "
        payload = {"name": name, "location": location}
        try:
            print(f"[CloudClient] Assigning pot {pot_id} to user at: {url}")
            response = requests.put(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("success", False)
        except requests.exceptions.RequestException as e:
            print(f"[CloudClient] ERROR: Could not assign pot. Details: {e}")
            return False

    def link_plant_to_pot(self, pot_id: str, user_token: str, plant_id: int) -> bool:
        """
        # Simulates a user linking a specific plant type to the pot.
        # This corresponds to `PUT /api/v1/Pots/{potId}/plant`.
        """
        url = f"{self.base_url}/api/v1/Pots/{pot_id}/plant"
        headers = {"Authorization": user_token}
        payload = {"plantId": plant_id}
        try:
            print(f"[CloudClient] Linking plant {plant_id} to pot {pot_id} at: {url}")
            response = requests.put(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("success", False)
        except requests.exceptions.RequestException as e:
            print(f"[CloudClient] ERROR: Could not link plant. Details: {e}")
            return False

    # --- Pot Operational Methods (Used during normal device operation) ---

    def get_thresholds_for_device(self, device_id: str) -> PotThreshold | None:
        """
        # Gets the operational thresholds for a device from the cloud's Planning context.
        # This is a critical PULL operation for the Edge device.
        """
        url = f"{self.base_url}/api/v1/devices/{device_id}/get-plant-thresholds"
        try:
            response = requests.get(url, timeout=10)
            # A 404 is an expected outcome if the device isn't configured yet.
            if response.status_code == 404:
                print(f"[CloudClient] No thresholds found on cloud for device {device_id}.")
                return None
            response.raise_for_status()
            data = response.json()
            # Translate the cloud's JSON resource into the edge's domain entity.
            return PotThreshold(
                device_id=device_id,
                temperature=Range(min=data["minTemp"], max=data["maxTemp"]),
                humidity=Range(min=data["minHumidity"], max=data["maxHumidity"]),
                light=Range(min=data["minLight"], max=data["maxLight"]),
                salinity=Range(min=data["minSalinity"], max=data["maxSalinity"]),
                ph=Range(min=data["minPh"], max=data["maxPh"]),
            )
        except requests.exceptions.RequestException as e:
            print(f"[CloudClient] ERROR: Network error fetching thresholds. Details: {e}")
            return None

    def update_pot_metrics_in_cloud(self, record: PotStateRecord) -> bool:
        """
        # Pushes a local PotStateRecord's metrics to the cloud's ARM endpoint.
        # This is a critical PUSH operation for the Edge device.
        """
        url = f"{self.base_url}/api/v1/Pots/{record.device_id}/metrics"
        # Translate the edge's domain entity into the cloud's expected JSON resource.
        payload = {
            "BatteryLevel": record.battery_level,
            "WaterLevel": record.water_level,
            "Humidity": record.humidity,
            "Luminance": record.light,
            "Temperature": record.temperature,
            "Ph": record.ph,
            "Salinity": record.salinity
        }
        try:
            response = requests.patch(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("success", False)
        except requests.exceptions.RequestException as e:
            print(f"[CloudClient] ERROR: Could not update pot metrics in cloud. Details: {e}")
            return False