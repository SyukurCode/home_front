from flask_login import current_user
from flask import jsonify
import config
import requests, json 
from datetime import datetime, date, timedelta
from apirequest import post_response, put_response
from dateutil.parser import parse 

import logwriter,os
current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

def get_token(username,password):
	payload = {
			'grant_type': 'password',
			'username': username,
			'password': password
		}
	try:
		response = requests.post(f'{config.api_endpoint}/api/login',
							headers={"Content-Type":"application/x-www-form-urlencoded"},
							data=payload)
			
		data = response.json()
		if response.status_code != 200:
			logger.logs(data)
			return None
			
		token = data['access_token']
		
	except requests.exceptions.RequestException as e:
			logger.logs(str(e))
			return None	
	
	return token

def executeTranslate(e):
	try:
		ex = json.loads(e['execute'])
	except Exception as er:
		logger.logs(f"Wrong format {str(er)}")
		logger.logs(f"execute:{e}")
		return None
	try:
		if e["event_repeat"]["name"] == 'Once' or e["repeat"] == 1:
			monthName = date(1900, int(ex["date"]["month"]), 1).strftime('%B')
			ampm = "AM"
			if e["event_type"]['name'] == "Prayer" or e["type"] == 2:
				time = datetime.strptime(ex["time"],'%H:%M')
				Hour12 = time.hour
				Minute = f'{time.minute}'
				if time.minute < 10:
					Minute = f'0{time.minute}'
				if time.hour > 12:
					Hour12 = time.hour - 12
					ampm = "PM"
				description = f'{ex["date"]["day"]} {monthName} {ex["date"]["year"]} '\
											+ f'{Hour12}:{Minute} {ampm}'
			else:
				Hour12 = ex["time"]["hour"]
				Minute = f'{ex["time"]["minute"]}'
				if ex["time"]["minute"] < 10:
					Minute = f'0{Minute}'
				if ex["time"]["hour"] > 12:
					Hour12 = ex["time"]["hour"] - 12
					ampm = "PM"

				description = f'{ex["date"]["day"]} {monthName} {ex["date"]["year"]} '\
						+ f'{Hour12}:{Minute} {ampm}'

		if e["event_repeat"]["name"] == 'Allday' or e["repeat"] == 2:
			monthName = date(1900, int(ex["date"]["month"]), 1).strftime('%B')
			description = f'{ex["date"]["day"]} {monthName} {ex["date"]["year"]} Every hours'

		if e["event_repeat"]["name"] == 'Daily' or e["repeat"] == 3:
			ampm = "AM"
			Hour12 = int(ex["time"]["hour"])
			Minute = f'{ex["time"]["minute"]}'
			if ex["time"]["minute"] < 10:
				Minute = f'0{Minute}'
			if ex["time"]["hour"] > 12:
				Hour12 = ex["time"]["hour"] - 12
				ampm = "PM"
			description = f'{ex["date"]["weekday"]}, {Hour12}:{Minute} {ampm}'

		if e["event_repeat"]["name"] == 'Monthly' or e["repeat"] == 4:
			description = f'Every {ex["date"]["day"]}'

		if e["event_repeat"]["name"] == 'Yearly' or e["repeat"] == 5:
			monthName = date(1900, int(ex["date"]["month"]), 1).strftime('%B')
			description = f'Every {ex["date"]["day"]} {monthName}'

		return description
	except Exception as er:
		logger.logs(f"Wrong format {str(er)}")
		logger.logs(f"execute:{e}")
		return None

def check_due(event):
	execute = json.loads(event['execute'])
	if event["event_repeat"]["name"] == "Once":
		if event["event_type"]["name"] == "Wish" or event["event_type"]['name'] == "Play":
			hour = execute["time"]["hour"]
			minute = execute["time"]["minute"]
		else:
			time = datetime.strptime(execute["time"],'%H:%M')
			hour = time.hour
			minute = time.minute
	elif event["event_repeat"]["name"] == "Allday":
		hour = 0
		minute = 0
	else:
		return json.dumps({'isDue': False,'minutes': 0})
    
	event_datetime = datetime(year=execute["date"]["year"],month=execute["date"]["month"],day=execute["date"]["day"],hour=hour,minute=minute,second=0)
	time_diff = datetime.now() - event_datetime
	period = time_diff.total_seconds()
	if period < 60:
		duration = f"{int(period)} seconds ago"
	elif period < 3600:
		duration = f"{int(period // 60)} minutes ago"
	elif period < 86400:
		duration = f"{int(period // 3600)} hours ago"
	elif period < 2592000:
		duration = f"{int(period // 86400)} days ago"
	elif period < 31536000:
		duration = f"{int(period // 2592000)} months ago"
	else:
		duration = f"{int(period // 31536000)} years ago"
	
	if period > 1.0 :
		return json.dumps({'isDue': True,'duration': duration})
	return json.dumps({'isDue': False,'duration': duration})

def get_next_weekday(weekday_name):
    # Dictionary to map weekday names to their respective numbers
    weekdays = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }

    # Ensure the input is lowercase
    weekday_name = weekday_name.lower()

    if weekday_name not in weekdays:
        raise ValueError("Invalid weekday name")

    # Get today's date and weekday number
    today = datetime.today()
    today_weekday = today.weekday()  # Monday is 0 and Sunday is 6

    # Get the target weekday number
    target_weekday = weekdays[weekday_name]

    # Calculate days until the target weekday
    days_ahead = target_weekday - today_weekday
    if days_ahead <= 0:  # Target day is in the next week
        days_ahead += 7

    # Calculate the date of the next target weekday
    next_weekday_date = today + timedelta(days=days_ahead)

    return next_weekday_date

def add_once(name,text,type,repeat,datetimepicker):
	dt = parse(datetimepicker)
	execute = '{"date":{"day":' + str(dt.day) + ',"month":' + str(dt.month) + ',"year":' + str(dt.year) + '}' \
			+ ',"time":{"hour":' + str(dt.hour) + ',"minute":' + str(dt.minute) + ',"second":' + str(dt.second) + '}}'
	return store_event(name,text,type,repeat,0,execute)

def add_allday(name,text,type,repeat,datepicker):
	d = parse(datepicker)
	execute = '{"date":{"day":' + str(d.day) + ',"month":' + str(d.month) + ',"year":' + str(d.year) + '}}'
	return store_event(name,text,type,repeat,0,execute)

def add_daily(name,text,type,repeat,timepicker,weekday):
	isFirst = True
	parent = 0
	t = parse(timepicker)
	for w in weekday:
		execute = '{"date":{"weekday":"' + w + '"},"time":{"hour":' + str(t.hour) + ',"minute":' + str(t.minute) + ',"second":' + str(t.second) + '}}'
		if isFirst:
			isFirst = False
			parent = store_event(name,text,type,repeat,0,execute)
		else:
			if not parent == 0:
				return store_event(name,text,type,repeat,parent,execute)
			else:
				logger.logs("daily store fail")
				return {"status":"fail","message":"store daily fail"}
def add_monthly(name,text,type,repeat,day):
	execute = '{"date":{"day":' + day + '}}'
	store_event(name,text,type,repeat,0,execute)

def add_yearly(name,text,type,repeat,day,month):
	execute = '{"date":{"day":' + day + ',"month":' + month + '}}'
	return store_event(name,text,type,repeat,0,execute)

def store_event(name,text,type,repeat,parent,execute):
	response = post_response('/api/event', \
							{"name": name,"text": text, \
							"type": type,"repeat": repeat, \
							"parent": parent,"execute": execute })
 
	if not isinstance(response, dict) or response.get('status_code') != 200:
				error_msg = response.get('error', 'Unknown error')
				return {"status":"fail", "message" : error_msg}
	
	data = response['data']
	id = data['id']
	#--update parent if not have parent--

	if data["parent"] == 0:
		update = put_response(f'/api/event/parent', \
							{"id":id,"parent": id})
  
		if not isinstance(response, dict) or response.get('status_code') != 200:
				error_msg = response.get('error', 'Unknown error')
				return {"status":"fail","message":error_msg}
		
		update_data = update

		logger.logs("event store success")
		return {"status":"success","message": update_data['data']['id']}

	else:
		logger.logs("event store request fail")
	return {"status": "fail", "message": "fail to store"}