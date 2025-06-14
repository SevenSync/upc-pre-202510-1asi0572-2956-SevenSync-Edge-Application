# operation/interfaces/controllers.py
from flask import Blueprint, request, jsonify, current_app

operation_api = Blueprint("operation_api", __name__)

@operation_api.route("/api/v1/operations/execute", methods=["POST"])
def execute_watering_operation():
    data = request.json
    device_id = data["device_id"]

    orchestrator = current_app.config["WATERING_ORCHESTRATOR"]
    execution = orchestrator.execute_watering_workflow(device_id)

    response = {
        "operation_id": execution.id,
        "device_id": execution.device_id,
        "duration": execution.duration,
        "success": execution.success,
        "executed_at": execution.timestamp.isoformat()
    }

    return jsonify(response), 200 if execution.success else 500