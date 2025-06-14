from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timezone

from iam.interfaces.services import authenticate_request

analytics_api = Blueprint("analytics_api", __name__)


@analytics_api.route("/api/v1/analytics/pot-record", methods=["POST"])
def create_pot_record():
    data = request.json
    try:
        # Obtener servicio inyectado desde app context
        app_service = current_app.config["POT_RECORD_SERVICE"]

        # Validar campos requeridos
        required_fields = ["device_id", "ph", "humidity", "temperature", "salinity", "light"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Crear registro usando el servicio
        record = app_service.create_pot_record(
            device_id=data["device_id"],
            sensor_data={
                "ph": data["ph"],
                "humidity": data["humidity"],
                "temperature": data["temperature"],
                "salinity": data["salinity"],
                "light": data["light"]
            },
            created_at=data.get("created_at"),
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
    data = request.json
    try:
        # Obtener servicio inyectado
        app_service = current_app.config["POT_RECORD_SERVICE"]

        # Validar campos requeridos
        required_fields = ["device_id", "ph", "humidity", "temperature", "salinity", "light"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Calcular tiempo usando el servicio de aplicación
        watering_seconds = app_service.calculate_watering_time(
            device_id=data["device_id"],
            sensor_data={
                "ph": data["ph"],
                "humidity": data["humidity"],
                "temperature": data["temperature"],
                "salinity": data["salinity"],
                "light": data["light"]
            },
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