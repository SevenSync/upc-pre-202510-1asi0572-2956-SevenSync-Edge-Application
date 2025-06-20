"""Interface services for the Pot Data context."""
from flask import Blueprint, request, jsonify
from analytics.application.services import PotRecordApplicationService
from iam.interfaces.services import authenticate_request

pot_data_api = Blueprint("pot_data_api", __name__)
app_service = PotRecordApplicationService()

@pot_data_api.route("/api/v1/analytics/pot-record", methods=["POST"])
def create_pot_record():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        record = app_service.create_pot_record(
            device_id=data["device_id"],
            sensor_data=data,
            created_at=data.get("created_at"),
            api_key=request.headers.get("X-API-Key")
        )
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "message": "Record created successfully."
        }), 201
    except (KeyError, TypeError):
        return jsonify({"error": "Missing or invalid required fields"}), 400
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400