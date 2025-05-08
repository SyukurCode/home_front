from flask import Blueprint, request, render_template, session, redirect
from datetime import datetime
from apirequest import get_user_avatar
import os,config, common
import requests, json # type: ignore
from apirequest import get_response
import logwriter,os
from model import calendar_model

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

kalendar = Blueprint('kalendar', __name__)
@kalendar.route('/calendar', methods=['GET'])
def index():
	token = common.session_get('Token')
	current_user = common.session_get('User')
	
	logger.logs("from:{},url:{}".format(request.remote_addr,request.url))

	viewdata = calendar_model(
		events = get_response('/api/event'),
		user = current_user,
		avatar = get_user_avatar(),
	).to_dict()
	return render_template("Calendar.html", **viewdata)


@kalendar.route('/calendar/api/all',methods=['GET'])
def allevent():
	logger.logs("from:{},url:{}".format(request.remote_addr,request.url))
	allEvents = []

	data = get_response('/api/event')

	if not isinstance(data, dict) or data.get('status_code') != 200:
		error_msg = data.get('data')
		return render_template("Login.html", **error_msg)
	
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

		if event['event_repeat']["name"] == 'Once' or event['repeat'] == 1:
			if event['event_type']["name"] == 'Prayer' or event['type'] == 2:
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

		if event['event_repeat']["name"] == 'Yearly' or event['repeat'] == 6:
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
    
