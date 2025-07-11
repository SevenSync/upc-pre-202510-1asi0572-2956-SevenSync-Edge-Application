from planning.domain.entities import PotThreshold
from shared.infrastructure.clients import CloudClient
from iam.application.services import AuthApplicationService

from planning.infrastructure.repositories import ThresholdRepository


class PlanningApplicationService:
    """
    # The Application Service for the Planning context.
    # REFACTORED to manage the caching of thresholds for resilience.
    """

    def __init__(
            self,
            cloud_client: CloudClient,
            auth_service: AuthApplicationService,
            threshold_repo: ThresholdRepository
    ):
        self.cloud_client = cloud_client
        self.auth_service = auth_service
        self.threshold_repo = threshold_repo

    def get_and_cache_thresholds(self, device_id: str) -> PotThreshold | None:
        """
        # This is the PRIMARY method to get thresholds. It tries to fetch from the cloud
        # and, upon success, updates the local cache.
        """
        print(f"[PlanningService] Attempting to fetch fresh thresholds from cloud for device {device_id}...")

        # 1. Try to get fresh data from the cloud.
        fresh_thresholds = self.cloud_client.get_thresholds_for_device(device_id)

        if fresh_thresholds:
            # 2. If successful, update the local cache with the new data.
            print(f"[PlanningService] Successfully fetched fresh thresholds. Updating local cache.")
            self.threshold_repo.save(fresh_thresholds)
            return fresh_thresholds
        else:
            # 3. If it fails, return None. The caller will handle the fallback.
            print(f"[PlanningService] WARNING: Could not fetch thresholds from cloud.")
            return None

    def get_cached_thresholds(self, device_id: str) -> PotThreshold | None:
        """
        # This is the FALLBACK method. It only reads from the local cache.
        """
        print(f"[PlanningService] Attempting to retrieve thresholds from local cache for device {device_id}...")
        cached_thresholds = self.threshold_repo.get_for_device(device_id)
        if cached_thresholds:
            print("[PlanningService] Found valid thresholds in local cache.")
        else:
            print("[PlanningService] WARNING: No thresholds found in local cache.")
        return cached_thresholds