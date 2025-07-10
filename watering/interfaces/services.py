from flask import Blueprint, request, jsonify, current_app

operation_api = Blueprint("operation_api", __name__)

@operation_api.route("/api/v1/operations/execute-cycle", methods=["POST"])
def execute_watering_operation():
    """
    # API endpoint to trigger a full operational cycle for a device.
    # This is the main entry point for an external scheduler (like cron) to run.
    """
    try:
        orchestrator = current_app.config["WATERING_ORCHESTRATOR"]
        api_key = request.headers.get("X-API-Key")
        device_id = request.json.get("deviceId")
        print(f"DEBUG: API received -> deviceId: '{device_id}', apiKey: '{api_key}'")

        if not api_key or not device_id:
            return jsonify({"error": "X-API-Key header and deviceId in body are required"}), 400

        result = orchestrator.execute_watering_cycle(device_id, api_key)

        return jsonify({
            "executedAt": result.timestamp.isoformat(),
            "deviceId": result.device_id,
            "actionTaken": result.duration_seconds > 0,
            "durationSeconds": result.duration_seconds,
            "wasSuccessful": result.success,
            "reasonForAction": result.reason
        }), 200

    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        current_app.logger.error(f"Error during watering cycle execution: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500