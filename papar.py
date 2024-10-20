from flask import Blueprint, request, current_app, render_template
from flask_login import current_user,login_required
from datetime import datetime, timezone
import requests, json, config # type: ignore

papar = Blueprint('papar', __name__)

@papar.route('/papar', methods=['GET'])
def index():
    state = request.args.get('state')
    device = request.args.get('device')
    response = requests.get(f'{config.api_endpoint}/smarthome/{device}?state={state}')
    if response.status_code == 200:
        status = response["status"]
        current = response["Date and Time"]
        return render_template("Papar.html",status=status.upper(),device=device,current=current)
    
