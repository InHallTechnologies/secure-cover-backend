from flask import Flask
from blueprints.user_blueprints import user_blueprints
from blueprints.report_blueprints import report_blueprint
from firebase_admin import initialize_app, credentials, db

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cred = credentials.ApplicationDefault()
initialize_app(cred, {"databaseURL": "https://cover-6c458-default-rtdb.firebaseio.com"})
app.register_blueprint(user_blueprints)
app.register_blueprint(report_blueprint)


@app.route("/", methods=["GET"])
def handle_test():
    return db.reference("/USER_ARCHIVE/0jYBHEIRPmZQWC8Nj0gGVQSVFiN2/name").get()
    

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
