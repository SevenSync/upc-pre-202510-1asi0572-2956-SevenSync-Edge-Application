"""Interface services for the Health-bounded context."""
from flask import Blueprint, request, jsonify

"""
from iam.interfaces.services import authenticate_request
"""

from anaytics.application.services import PotRecordApplicationService

analytics_api = Blueprint("analytics_api", __name__)

# Initialize dependencies
pot_record_service = PotRecordApplicationService()

@analytics_api.route("/api/v1/analytics/pot-record", methods=["POST"])
def create_health_record():
    """Handle POST requests to create a health record.

    Expects JSON with device_id, ph, humidity, temperature, salinity, light and created_at.

    Returns:
        tuple: (JSON response, status code).
    """
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        device_id = data["device_id"]
        ph = data["ph"]
        humidity = data["humidity"]
        temperature = data["temperature"]
        salinity = data["salinity"]
        light = data["light"]
        created_at = data.get("created_at")
        record = pot_record_service.create_record(
            device_id, ph, humidity, temperature, salinity, light, created_at, request.headers.get("X-API-Key")
        )
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "ph": record.ph,
            "humidity": record.humidity,
            "temperature": record.temperature,
            "salinity": record.salinity,
            "light": record.light,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400