"""Flask application entry point for the MaceTech Edge Service."""
from flask import Flask
from shared.infrastructure.database import db, init_db_tables
# --- Importar todos los blueprints ---
from iam.interfaces.controllers import iam_api
from analytics.interfaces.services import analytics_api
from watering.interfaces.services import watering_api
from planning.interfaces.controllers import planning_api # <-- NUEVA IMPORTACIÓN
from iam.application.services import AuthApplicationService

app = Flask(__name__)

# --- Registrar todos los Bounded Contexts ---
app.register_blueprint(iam_api)
app.register_blueprint(analytics_api)
app.register_blueprint(watering_api)
app.register_blueprint(planning_api) # <-- NUEVO REGISTRO

# ... (el resto del archivo permanece igual)
@app.before_request
def before_request_handler():
    db.connect()

@app.after_request
def after_request_handler(response):
    if not db.is_closed():
        db.close()
    return response

if __name__ == "__main__":
    db.connect()
    init_db_tables()
    auth_service = AuthApplicationService()
    auth_service.get_or_create_test_device()
    db.close()
    app.run(host='0.0.0.0', port=5000, debug=True)