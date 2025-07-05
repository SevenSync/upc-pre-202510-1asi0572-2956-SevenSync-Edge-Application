"""Flask application entry point for the MaceTech Edge Service."""
from flask import Flask
from shared.infrastructure.database import db, init_db_tables
from watering.interfaces.services import operation_api
from planning.interfaces.controllers import planning_api
from iam.application.services import AuthApplicationService

app = Flask(__name__)

app.register_blueprint(iam_api)
app.register_blueprint(analytics_api)
app.register_blueprint(operation_api)
app.register_blueprint(planning_api)

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