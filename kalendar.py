from flask import Blueprint, Flask, request, jsonify, current_app, render_template
from flask_login import current_user,LoginManager,login_user,logout_user,login_required
from models import db,User
from datetime import datetime
from flask_bcrypt import Bcrypt
from dateutil.parser import parse # type: ignore
import os
import common
import requests, json # type: ignore
import logging


api_host = os.environ['API_HOST']
api_port = os.environ['API_PORT']
endpoint = "http://{}:{}".format(api_host,api_port)

kalendar = Blueprint('kalendar', __name__)
@login_required
@kalendar.route('/calendar', methods=['GET'])
def index():
	return render_template("Calendar.html")


@kalendar.route('/calendar/api/all',methods=['GET'])
def allevent():
	allEvents = []
	token = common.get_token(current_user.username,current_user.publicId)

	try:
		response = requests.get(f'{endpoint}/api/event',headers={"x-access-tokens": token})
	except Exception as e:
		logging.debug("Exception")
		return None

	if response.status_code == 200:
		data = response.json()
		events = data['data']
		for event in events:
			_groupId = event["parent"]
			_title = event["name"]
			_id = event["id"]
			_start = ""
			try:
				dateTimeJson = json.loads(event['execute'])
			except Exception as e:
				logging.debug("Wrong format")


			if event['repeat'] == 'Once' or event['repeat'] == 1:
				if event['type'] == 'Prayer' or event['type'] == 2:
					time = datetime.strptime(dateTimeJson["time"],'%H:%M')
					Hour = time.hour
					Minute = time.minute
					Day = dateTimeJson['date']['day']
					Month = dateTimeJson['date']['month']
					Year = dateTimeJson['date']['year']

					_start = f"{Year}-{Month:02d}-{Day:02d}T{Hour:02d}:{Minute:02d}:00"
				else:
					Hour = dateTimeJson['time']['hour']
					Minute = dateTimeJson['time']['minute']
					Day = dateTimeJson['date']['day']
					Month = dateTimeJson['date']['month']
					Year = dateTimeJson['date']['year']

					_start = f"{Year}-{Month:02d}-{Day:02d}T{Hour:02d}:{Minute:02d}:00"

			if event['repeat'] == 'Allday' or event['repeat'] == 2:
				#Hour = dateTimeJson['time']['hour']
				#Minute = dateTimeJson['time']['minute']
				Day = dateTimeJson['date']['day']
				Month = dateTimeJson['date']['month']
				Year = dateTimeJson['date']['year']

				_start = f"{Year}-{Month:02d}-{Day:02d}"

			#if event['repeat'] == 'Daily' or event['repeat'] == 3:
				#Hour = dateTimeJson['time']['hour']
				#Minute = dateTimeJson['time']['minute']
				#Day = dateTimeJson['date']['day']
				#Month = dateTimeJson['date']['month']
				#Year = dateTimeJson['date']['year']

				#_start = f"{Year:02d}-{Month:02d}-{Day:02d}"

			if event['repeat'] == 'Monthly' or event['repeat'] == 5:
				Year = datetime.now().year
				Month = datetime.now().month
				#Hour = dateTimeJson['time']['hour']
				#Minute = dateTimeJson['time']['minute']
				Day = dateTimeJson['date']['day']
				#Month = dateTimeJson['date']['month']
				#Year = dateTimeJson['date']['year']

				_start = f"{Year}-{Month:02d}-{Day:02d}"

			if event['repeat'] == 'Yearly' or event['repeat'] == 6:
				Year = datetime.now().year
                                #Hour = dateTimeJson['time']['hour']
                                #Minute = dateTimeJson['time']['minute']
				Day = dateTimeJson['date']['day']
				Month = dateTimeJson['date']['month']
                                #Year = dateTimeJson['date']['year']

				_start = f"{Year}-{Month:02d}-{Day:02d}"

			current_event = {
				'groupId': _groupId,
				'title': _title,
				'start': _start,
				'url': '/detail?id=' + str(_id)
				}
			allEvents.append(current_event)
		return allEvents
	return None
    
