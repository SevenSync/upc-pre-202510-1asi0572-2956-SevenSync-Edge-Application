"""Interface controllers for the Planning context."""
from flask import Blueprint, jsonify
from planning.application.services import PlanningApplicationService

planning_api = Blueprint("planning_api", __name__)
app_service = PlanningApplicationService()

@planning_api.route("/api/v1/planning/devices/<device_id>/decision", methods=["GET"])
def get_device_watering_decision(device_id: str):
    try:
        decision = app_service.get_watering_decision(device_id)
        return jsonify({
            "should_water": decision.should_water,
            "duration_seconds": decision.duration_seconds
        }), 200
    except Exception as e:
        # En un sistema real, aquí habría un logging más detallado
        return jsonify({"error": f"Error al calcular la decisión: {e}"}), 500