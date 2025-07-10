from flask import Blueprint, request, jsonify, current_app

arm_api = Blueprint("arm_api", __name__)


@arm_api.route("/api/v1/arm/state-records", methods=["POST"])
def create_state_record():
    """
    # API endpoint to allow the device hardware to post its sensor readings.
    """
    arm_service = current_app.config["ARM_APP_SERVICE"]
    api_key = request.headers.get("X-API-Key")
    data = request.json

    try:
        device_id = data.pop("device_id")
        if not api_key:
            return jsonify({"error": "Missing X-API-Key header"}), 401

        record = arm_service.create_state_record(device_id, api_key, **data)

        return jsonify({"message": "Record created successfully", "id": record.id}), 201

    except KeyError:
        return jsonify({"error": "Missing 'device_id' in request body"}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        current_app.logger.error(f"Error creating state record: {e}")
        return jsonify({"error": "Internal server error"}), 500