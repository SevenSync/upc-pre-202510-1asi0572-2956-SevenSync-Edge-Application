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


# analytics/interfaces/controllers.py
@analytics_api.route("/api/v1/analytics/device-status/<device_id>", methods=["GET"])
@authenticate_request
def get_device_status(device_id: str):
    try:
        # Obtener servicio desde la app
        app_service = current_app.config["POT_RECORD_SERVICE"]

        # 1. Obtener última lectura
        last_record = app_service.get_last_record(device_id)

        # 2. Obtener umbrales desde el servicio de thresholds
        thresholds = app_service.threshold_service.get_thresholds(device_id)

        # 3. Preparar respuesta
        return jsonify({
            "device_id": device_id,
            "last_record": {
                "humidity": last_record.humidity,
                "temperature": last_record.temperature,
                "light": last_record.light,
                "ph": last_record.ph,
                "salinity": last_record.salinity,
                "created_at": last_record.created_at.isoformat() + "Z"
            },
            "thresholds": thresholds,
            "calculated_watering_seconds": WateringCalculator.calculate(
                sensor_data={
                    "humidity": last_record.humidity,
                    "temperature": last_record.temperature,
                    "light": last_record.light,
                    "ph": last_record.ph,
                    "salinity": last_record.salinity
                },
                thresholds=thresholds
            )
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        current_app.logger.error(f"Device status error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500