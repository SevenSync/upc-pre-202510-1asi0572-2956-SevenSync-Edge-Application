"""
Interface controllers for the IAM bounded context.
Defines API endpoints and request handlers.
"""
from flask import Blueprint, request, jsonify
from iam.application.services import AuthApplicationService

# --- Definición del Blueprint ---
# iam_api se define aquí, como una colección de rutas para este contexto.
iam_api = Blueprint("iam_api", __name__)

# --- Dependencias ---
auth_service = AuthApplicationService()


# --- Helpers / Decoradores de Autenticación ---
def authenticate_request():
    """
    Authenticates an incoming HTTP request.
    This function is used by other controllers to protect njihove rute.
    """
    device_id = request.json.get("device_id") if request.json else None
    api_key = request.headers.get("X-API-Key")

    if not device_id or not api_key:
        return jsonify({"error": "Missing device_id or X-API-Key"}), 401

    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid device_id or API key"}), 401

    return None  # La autenticación es exitosa