from flask import Blueprint, redirect, render_template, session
from apirequest import get_user_avatar
# from datetime import datetime, timezone
import requests, config # type: ignore
import logwriter,os

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

maps = Blueprint('maps', __name__)

@maps.route('/maps', methods=['GET'])
def index():
    token = session.get('Token')
    if not token:
        return redirect("/logout")
    current_user = session.get('User')
    
    viewdata = {
        "user": current_user,
        "avatar" : get_user_avatar(),
        "apikey" : 'AIzaSyBrAu0iVt8uqJ_t7YF9q6o1Wj7Jb3ZNkBQ'
    }
    return render_template("Maps.html", **viewdata)