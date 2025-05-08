from flask import Blueprint, session, render_template, redirect
from datetime import datetime
import logwriter,os,json, common
from apirequest import get_user_avatar, get_response

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

waktu_solat = Blueprint('wakto_solat', __name__)

@waktu_solat.route("/waktu_solat", methods = ["GET"])
def index():
    current_user = common.session_get("User")
    waktu = []
    response = get_response('/api/event')
    
    data = response["data"]
    for item in data:
        if item["event_type"]["name"] == "Prayer":
            execute = json.loads(item['execute'])
            time = datetime.strptime(execute["time"],'%H:%M')
            waktu.append({"name":item["name"], "time":time.strftime('%I:%M %p')})

    viewdata = {
		"user" : current_user,
		"avatar" : get_user_avatar(),
        "waktu_solat" : waktu,
	}
    # return jsonify({**viewdata}),200
    return render_template("WaktuSolat.html", **viewdata)
    
