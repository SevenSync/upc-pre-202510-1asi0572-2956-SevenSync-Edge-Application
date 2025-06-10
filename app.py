from flask import Flask

import iam.application.services
from shared.infrastructure.database import init_db

app = Flask(__name__)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        # Initialize the database here
        init_db()
        auth_application_service = iam.application.services.AuthApplicationService()
        auth_application_service.get_or_create_test_device()

if __name__ == '__main__':
    app.run(debug=True)