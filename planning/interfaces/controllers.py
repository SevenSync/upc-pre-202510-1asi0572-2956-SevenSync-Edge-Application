from flask import Blueprint, jsonify, current_app, request

planning_api = Blueprint("planning_api", __name__)

@planning_api.route("/api/v1/planning/devices/<device_id>/decision", methods=["GET"])
def get_device_watering_decision(device_id: str):
    try:
        app_service = current_app.config["PLANNING_APP_SERVICE"]
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return jsonify({"error": "X-API-Key header is required"}), 401

        decision = app_service.get_watering_decision(device_id, api_key)
        return jsonify({
            "should_water": decision.should_water,
            "duration_seconds": decision.duration_seconds,
            "reason": decision.reason,
            "device_id": device_id
        }), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        current_app.logger.error(f"Error calculating decision for {device_id}: {e}")
        return jsonify({"error": "An internal error occurred."}), 500