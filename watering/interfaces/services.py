"""Interface services for the Watering context (versión simplificada)."""
from flask import Blueprint, request, jsonify
from watering.application.services import WateringApplicationService
from iam.interfaces.controllers import authenticate_request

watering_api = Blueprint("watering_api", __name__)
app_service = WateringApplicationService()

@watering_api.route("/api/v1/operations/execute", methods=["POST"])
def execute_watering():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        # La lógica compleja ahora está oculta detrás de este servicio
        decision = app_service.execute_and_log_operation(
            device_id=data["device_id"],
            api_key=request.headers.get("X-API-Key")
        )
        # Se devuelve directamente la respuesta de Planning
        return jsonify(decision), 200
    except (KeyError, TypeError):
        return jsonify({"error": "Missing device_id"}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401