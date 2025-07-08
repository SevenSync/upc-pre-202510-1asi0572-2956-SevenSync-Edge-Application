"""Interface services for the IAM bounded context."""
from flask import request, jsonify
from iam.application.services import AuthApplicationService

auth_service = AuthApplicationService()

def authenticate_request():
    device_id = request.json.get("device_id") if request.json else None
    api_key = request.headers.get("X-API-Key")

    if request.method == 'GET' and not device_id:
        pass

    if not device_id or not api_key:
        return jsonify({"error": "Missing device_id or X-API-Key"}), 401

    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid device_id or API key"}), 401

    return None