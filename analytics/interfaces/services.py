from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timezone

from analytics.application.services import PotRecordApplicationService
from iam.interfaces.services import authenticate_request


analytics_api = Blueprint("analytics_api", __name__)

pot_record_service = PotRecordApplicationService()

@analytics_api.route("/api/v1/analytics/records", methods=["POST"])
def create_pot_record_on_backend():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json

    try:
        device_id = data["device_id"]
        temperature = data["temperature"]
        humidity = data["humidity"]
        light = data["light"]
        salinity = data["salinity"]
        ph = data["ph"]
        created_at = data.get("created_at", datetime.now(timezone.utc).isoformat() + "Z")

        record = pot_record_service.create_pot_record(
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            light=light,
            salinity=salinity,
            ph=ph,
            created_at=created_at,
            api_key=request.headers.get("X-API-Key")
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
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401


@analytics_api.route("/api/v1/analytics/calculate-time-watering", methods=["POST"])
def calculate_watering_time():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json

    try:
        device_id = data["device_id"]

        watering_seconds = pot_record_service.calculate_watering_time(
            device_id,
            api_key=request.headers.get("X-API-Key")
        )

        return jsonify({
            "device_id": data["device_id"],
            "watering_time_seconds": watering_seconds,
            "calculated_at": datetime.now(timezone.utc).isoformat() + "Z"
        }), 200
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        current_app.logger.error(f"Unhandled error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@analytics_api.route("/api/v1/analytics/device-status/<device_id>/records", methods=["POST"])
def get_device_status(device_id: str):
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json

    try:
        device_id = data["device_id"]

        records = pot_record_service.get_records_by_device_id(
            device_id,
            api_key=request.headers.get("X-API-Key")
        )

        return jsonify({
            "device_id": device_id,
            "records": [
                {
                    "id": record.id,
                    "temperature": record.temperature,
                    "humidity": record.humidity,
                    "light": record.light,
                    "salinity": record.salinity,
                    "ph": record.ph,
                    "created_at": record.created_at.isoformat() + "Z"
                } for record in records
            ]
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        current_app.logger.error(f"Device status error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500