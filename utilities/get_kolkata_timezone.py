from datetime import datetime
import pytz

def get_kolkata_date_time():
    tz = pytz.timezone('Asia/Kolkata')
    kolkata_now = datetime.now(tz)
    return kolkata_now.strftime("%d-%m-%Y %I:%M %p")

def get_kolkata_date():
    tz = pytz.timezone('Asia/Kolkata')
    kolkata_now = datetime.now(tz)
    return kolkata_now.strftime("%d-%m-%Y")