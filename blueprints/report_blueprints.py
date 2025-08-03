from flask import Blueprint, request, send_file
from firebase_admin import db
from constants.admin_uids import admin_uid
import pandas as pd
import numpy as np
from io import BytesIO
import math

report_blueprint = Blueprint('reporting_blueprint',__name__, url_prefix="/reporting")

@report_blueprint.route("/call_report", methods=["POST"])
def download_call_logs():
    print("Hello")
    arguments = request.get_json(silent=True)
    request_uid = request.headers.get("X-Admin-Uid", "")

    if request_uid not in admin_uid:
        return {"message": "Unauthorized", "status": 401}, 401
    if not arguments:
        return {"message": "Bad Request", "status": 400}, 400

    date = arguments.get("date", None)
    date = date.split("-")[::-1]
    date = "-".join(date)
    print(date)
    if not date:
        return {"message": "Bad Request", "status": 400}, 400
    
    users = db.reference("/USER_ARCHIVE").get()
    users_list = list(users.keys())

    data = []
    for uid in users_list:
        call_logs = db.reference("/NEW_CALL_LOGS").child(uid).child(date).get()
        if call_logs:
            call_list = list(call_logs.values())
            new_list = []
            for log in call_list:
                log['advisorName'] = users[uid]['name']
                if "callDurationInSeconds" in log:
                    log['callDurationInSeconds'] = abs(int(log["callDurationInSeconds"]))
                new_list.append(log)

            data = data + new_list


    call_logs_dataframe = pd.DataFrame.from_records(data)
    call_logs_dataframe.replace(np.nan, None, inplace=True)

    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        call_logs_dataframe.to_excel(writer, index=False, sheet_name=f"calling_report_{date}")
    buf.seek(0)
    print("COmpleteed")
    call_logs_dataframe.to_excel("./temp.xlsx")
    return send_file(
        buf,
        as_attachment=True,
        download_name=f"calling_report_{date}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    
