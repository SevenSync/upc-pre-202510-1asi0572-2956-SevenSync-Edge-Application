# /cloud_sync/application/services.py
from shared.infrastructure.clients import CloudClient
from arm.application.services import ArmApplicationService


class CloudSyncService:
    """
    # Application service to orchestrate synchronization workflows with the cloud.
    # It acts as a "logistics manager" for complex cloud interactions,
    # keeping this complexity out of the main operational contexts.
    """

    def __init__(self, cloud_client: CloudClient, arm_service: ArmApplicationService):
        self.cloud_client = cloud_client
        self.arm_service = arm_service

    def provision_new_device(self, user_token: str, plant_id: int, pot_name: str, pot_location: str) -> str | None:
        """
        # Executes the full provisioning workflow for testing and simulation purposes.
        # This simulates what a user's mobile app would do in several steps.
        # 1. Creates a pot entity in the cloud.
        # 2. Assigns that pot to the user.
        # 3. Links a specific plant type to the pot.
        # Returns the new pot_id if the entire workflow is successful.
        """
        print("--- Starting New Device Provisioning Workflow ---")
        pot_id = self.cloud_client.create_pot_in_cloud()
        if not pot_id:
            print("WORKFLOW FAILED at Step 1: Pot Creation in Cloud.")
            return None
        print(f"Step 1 [SUCCESS]: Pot created in cloud with ID: {pot_id}")

        assign_ok = self.cloud_client.assign_pot_to_user(pot_id, user_token, pot_name, pot_location)
        if not assign_ok:
            print(f"WORKFLOW FAILED at Step 2: Assigning Pot {pot_id} to user.")
            return None
        print(f"Step 2 [SUCCESS]: Pot {pot_id} assigned to user.")

        link_ok = self.cloud_client.link_plant_to_pot(pot_id, user_token, plant_id)
        if not link_ok:
            print(f"WORKFLOW FAILED at Step 3: Linking Plant {plant_id} to Pot {pot_id}.")
            return None
        print(f"Step 3 [SUCCESS]: Plant {plant_id} linked to Pot {pot_id}.")
        print("--- Provisioning Workflow Completed Successfully ---")
        return pot_id

    def sync_latest_record_to_cloud(self, device_id: str, api_key: str) -> bool:
        """
        # Orchestrates a data PUSH operation.
        # 1. Gets the latest state record from the local ARM context.
        # 2. Pushes that record to the cloud's ARM endpoint.
        """
        print(f"--- Syncing latest record for device '{device_id}' to cloud ---")
        local_record = self.arm_service.get_last_state_record(device_id, api_key)

        if not local_record:
            print("No local record found to sync.")
            return False

        print(f"Found local record to sync: {local_record.__dict__}")
        success = self.cloud_client.update_pot_metrics_in_cloud(local_record)
        print(f"Sync to cloud successful: {success}")
        return success