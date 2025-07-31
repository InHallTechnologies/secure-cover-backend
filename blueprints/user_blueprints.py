from flask import Blueprint, request
from firebase_admin import auth, db
from constants.admin_uids import admin_uid
from utilities.get_kolkata_timezone import get_kolkata_date_time


user_blueprints = Blueprint("user_blueprint", __name__, url_prefix="/handle-user")


@user_blueprints.route("/onboard-user", methods=["POST"])
def onboard_user():
    arguments = request.get_json(silent=True)
    request_uid = request.headers.get("X-Admin-Uid", "")
    

    if request_uid not in admin_uid:
        return {"message": "Unauthorized", "status": 401}, 401
    if not arguments:
        return {"message": "Bad Request", "status": 400}, 400

    email_id = arguments.get("emailId", None)
    password = arguments.get("password", None)

    all_users = list(db.reference("/USER_ARCHIVE").get().values())
    print(all_users)
    found_item = [user for user in all_users if user['emailId'] == email_id]

    if (len(found_item) != 0):
        return {"message": "Email already registered", "status": 400}, 400

    if not email_id:
        return {"message": "Bad Request", "status": 400}, 400

    if not password:
        return {"message": "Bad Request", "status": 400}, 400

    try:
        user = auth.create_user(email=email_id, password=password)
        print(arguments)
        arguments["accountCreatedOn"] = get_kolkata_date_time()
        arguments['uid'] = user.uid
        db.reference("USER_ARCHIVE").child(user.uid).set(arguments)
        return {"message": "Success", "uid": user.uid}, 200
    except auth.EmailAlreadyExistsError:
        return {"message": "Email Already Exists", "status": 400}, 400


@user_blueprints.route("/disable-user", methods=["POST"])
def disable_user():
    arguments = request.get_json(silent=True)
    request_uid = request.headers.get("X-Admin-Uid", "")

    if request_uid not in admin_uid:
        return {"message": "Unauthorized", "status": 401}, 401
    if not arguments:
        return {"message": "Bad Request", "status": 400}, 400
    
    uid = arguments.get("uid", None)
    try:
        auth.update_user(uid, {"disabled": False})
        db.reference("USER_ARCHIVE").child(uid).child("status").set("In-Active")
        return {"message": "Success", "uid": uid}, 200
    except: 
        return {"message": "Something went wrong", "status": 500}, 500
