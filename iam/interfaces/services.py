"""Interface services for the IAM bounded context."""
from flask import request, jsonify
from iam.application.services import AuthApplicationService

# Initialize dependencies
auth_service = AuthApplicationService()

def authenticate_request():
    """Authenticates a request. To be used as a dependency by other interfaces."""
    device_id = request.json.get("device_id") if request.json else None
    api_key = request.headers.get("X-API-Key")

    # For GET requests, device_id might be in the URL, not JSON body
    if request.method == 'GET' and not device_id:
        # This is a simplification; a real app might pass args differently.
        # This decorator is primarily for POSTs as designed in the example.
        pass

    if not device_id or not api_key:
        return jsonify({"error": "Missing device_id or X-API-Key"}), 401

    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid device_id or API key"}), 401

    return None