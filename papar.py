from flask import Blueprint, request, render_template
# from datetime import datetime, timezone
import requests, config # type: ignore
import logwriter,os

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

papar = Blueprint('papar', __name__)

@papar.route('/papar', methods=['GET'])
def index():
    logger.logs("from:{},url:{}".format(request.remote_addr,request.url))
    state = request.args.get('state')
    device = request.args.get('device')
    token = get_token("admin","syukur123***")
    response = requests.get(f'{config.api_endpoint}/api/smarthome/{device}?state={state}',
                            headers={"accept": "application/json",
								"Authorization":f"Bearer {token}"})
    if response.status_code == 200:
        data = response.json()
        status = data["status"]
        current = data["Date and Time"]
        return render_template("Papar.html",status=status.upper(),device=device,current=current)
    return ({"Message":"Api fail to response"})
    
def get_token(username: str, password: str):
    payload = {
			'grant_type': 'password',
			'username': username,
			'password': password
		}

    response = requests.post(f'{config.api_endpoint}/api/login',
                    headers={"Content-Type":"application/x-www-form-urlencoded"},
                    data=payload)
    data = response.json()
    if response.status_code != 200:
        return None
    
    token = data['access_token']
    return token