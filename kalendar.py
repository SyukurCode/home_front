from flask import Blueprint, request, current_app, render_template, session, redirect
from flask_login import current_user,login_required
from datetime import datetime
from flask_bcrypt import Bcrypt
from dateutil.parser import parse # type: ignore
from apirequest import get_user_avatar
import os,config
import requests, json # type: ignore

import logwriter,os

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

kalendar = Blueprint('kalendar', __name__)
@login_required
@kalendar.route('/calendar', methods=['GET'])
def index():
	token = session.get('Token')
	current_user = session.get('User')
	if not token:
		return redirect("/logout")
	
	logger.logs("from:{},url:{}".format(request.remote_addr,request.url))

	viewdata = {
		"user" : current_user,
		"avatar" : get_user_avatar(),
	}

	return render_template("Calendar.html", **viewdata)


@kalendar.route('/calendar/api/all',methods=['GET'])
def allevent():
	token = session.get('Token')
	current_user = session.get('User')
	if not token:
		return redirect("/logout")
	
	logger.logs("from:{},url:{}".format(request.remote_addr,request.url))
	allEvents = []

	response = requests.get(f'{config.api_endpoint}/api/event',
						headers={"accept": "application/json",
							"Authorization":f"Bearer {token}"})
	
	data = response.json()
	
	if response.status_code != 200:
		logger.logs(data)
		session.clear()
		return render_template("Login.html",error=data['detail'])
	
	events = data['data']
	for event in events:
		_groupId = event["parent"]
		_title = event["name"]
		_id = event["id"]
		_start = ""
		try:
			dateTimeJson = json.loads(event['execute'])
		except Exception as e:
			logger.logs("Wrong format")

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
    
