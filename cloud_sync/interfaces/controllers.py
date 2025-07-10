# /cloud_sync/interfaces/controllers.py
from flask import Blueprint, request, jsonify, current_app

# This blueprint provides developer/testing endpoints for cloud interactions.
cloud_sync_api = Blueprint("cloud_sync_api", __name__)


@cloud_sync_api.route("/api/v1/testing/provision-device", methods=["POST"])
def provision_device():
    """
    # A test endpoint to simulate the entire device onboarding process.
    # It allows a developer to create and configure a new pot in the cloud
    # with a single API call, without needing a real mobile app.
    #
    # Requires:
    # - Header: "Authorization": "Bearer <user_jwt_token>"
    # - Body (JSON): { "plantId": 123, "name": "My Test Pot", "location": "Office" }
    """
    try:
        sync_service = current_app.config["CLOUD_SYNC_SERVICE"]

        # In a real scenario, this token would be from a user login.
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Authorization header is required"}), 401

        data = request.json
        plant_id = data.get("plantId")
        pot_name = data.get("name", "Test Pot")
        pot_location = data.get("location", "Test Location")

        if not plant_id:
            return jsonify({"error": "plantId is a required field in the JSON body"}), 400

        new_pot_id = sync_service.provision_new_device(token, plant_id, pot_name, pot_location)

        if new_pot_id:
            return jsonify({"message": "Device provisioned successfully", "newPotId": new_pot_id}), 201
        else:
            return jsonify({"error": "Failed to provision device during multi-step workflow"}), 500
    except Exception as e:
        current_app.logger.error(f"Error during provisioning: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500


@cloud_sync_api.route("/api/v1/testing/sync-record", methods=["POST"])
def sync_record():
    """
    # A test endpoint to manually trigger a push of the latest local sensor data to the cloud.
    #
    # Requires:
    # - Header: "X-API-Key": "<device_api_key>"
    # - Body (JSON): { "deviceId": "your-device-id" }
    """
    try:
        sync_service = current_app.config["CLOUD_SYNC_SERVICE"]
        api_key = request.headers.get("X-API-Key")
        device_id = request.json.get("deviceId")

        if not api_key or not device_id:
            return jsonify({"error": "X-API-Key header and deviceId in body are required"}), 400

        success = sync_service.sync_latest_record_to_cloud(device_id, api_key)

        if success:
            return jsonify({"message": "Record synced to cloud successfully"}), 200
        else:
            return jsonify({"error": "Failed to sync record to cloud"}), 500
    except Exception as e:
        current_app.logger.error(f"Error during record sync: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500