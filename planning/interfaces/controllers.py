from flask import Blueprint, jsonify, current_app, request

# This blueprint exposes the 'thinking' capability of the Planning context.
planning_api = Blueprint("planning_api", __name__)


@planning_api.route("/api/v1/planning/devices/<device_id>/decision", methods=["GET"])
def get_device_watering_decision(device_id: str):
    """
    # API endpoint to request a watering decision for a specific device.
    # This is a 'pull' model, where an external actor (like the watering orchestrator)
    # can ask the planning context "what should I do now?".
    """
    try:
        # Get the fully constructed application service from the app's config.
        app_service = current_app.config["PLANNING_APP_SERVICE"]
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return jsonify({"error": "X-API-Key header is required"}), 401

        decision = app_service.get_watering_decision(device_id, api_key)

        return jsonify({
            "deviceId": device_id,
            "shouldWater": decision.should_water,
            "durationSeconds": decision.duration_seconds,
            "reason": decision.reason
        }), 200

    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        current_app.logger.error(f"Error calculating decision for {device_id}: {e}")
        return jsonify({"error": "An internal error occurred."}), 500