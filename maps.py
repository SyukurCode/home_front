from flask import Blueprint, request, render_template, session
# from datetime import datetime, timezone
import requests, config # type: ignore
import logwriter,os

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

maps = Blueprint('maps', __name__)

@maps.route('/maps', methods=['GET'])
def index():
    token = session.get('Token')
    current_user = session.get('User')
    
    viewdata = {
        "user": current_user
    }
    return render_template("Maps.html", **viewdata)