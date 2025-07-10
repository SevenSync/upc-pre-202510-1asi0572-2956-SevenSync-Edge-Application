# /iam/interfaces/services.py

from flask import Blueprint, request, jsonify, current_app

iam_api = Blueprint("iam_api", __name__)

def authenticate_request():
    """
    # This function provides a reusable authentication check for any endpoint.
    # REFACTORED to fetch the correctly configured AuthApplicationService
    # from the application context (via current_app.config).
    """
    # Fetch the single, correct instance of the service from the Composition Root.
    auth_service = current_app.config["AUTH_APP_SERVICE"]
    
    # The deviceId might be in the URL path or in the JSON body.
    # This helper should be flexible. For now, it assumes JSON body.
    device_id = request.json.get("device_id") if request.json else None
    api_key = request.headers.get("X-API-Key")

    if not device_id or not api_key:
        # Return the error response directly, as this is used as a guard.
        return jsonify({"error": "Missing device_id in body or X-API-Key in headers"}), 401

    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid device_id or API key"}), 403 # 403 Forbidden is more accurate here

    # If authentication succeeds, return None to let the original endpoint continue.
    return None

# ADDED: A test endpoint within the IAM context itself.
@iam_api.route("/api/v1/iam/authenticate", methods=["POST"])
def check_authentication():
    """
    # A standalone endpoint to test the authentication mechanism.
    """
    auth_result = authenticate_request()
    
    if auth_result:
        # If authenticate_request returned an error response, forward it.
        return auth_result
    
    # If authenticate_request returned None, it means success.
    return jsonify({"message": "Authentication successful"}), 200