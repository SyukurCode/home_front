from flask import Blueprint, request, current_app, render_template
from flask_login import current_user,login_required
from datetime import datetime, timezone
import requests, json, config # type: ignore
import logwriter,os

current_directory = os.getcwd()
logger = logwriter.writer(current_directory + "/logs/","gui",__name__)

papar = Blueprint('papar', __name__)

@papar.route('/papar', methods=['GET'])
def index():
    logger.logs("from:{},url:{}".format(request.remote_addr,request.url))
    state = request.args.get('state')
    device = request.args.get('device')
    token = get_token("admin","syukur123***")
    response = requests.get(f'{config.api_endpoint}/api/smarthome/{device}?state={state}',headers={"x-access-tokens": token})
    if response.status_code == 200:
        data = response.json()
        status = data["status"]
        current = data["Date and Time"]
        return render_template("Papar.html",status=status.upper(),device=device,current=current)
    return ({"Message":"Api fail to response"})
    
def get_token(username: str, password: str):
    response = requests.post(f'{config.api_endpoint}/api/login', auth = (username, password))
    if response.status_code == 200:
        data = response.json()
        token = data['token']
        return token
    return None