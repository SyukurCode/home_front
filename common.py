from flask_login import current_user
import config
import requests, json # type: ignore
from datetime import datetime, date, timedelta

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
		if e["repeat"] == 'Once' or e["repeat"] == 1:
			monthName = date(1900, int(ex["date"]["month"]), 1).strftime('%B')
			ampm = "AM"
			if e["type"] == "Prayer" or e["type"] == 2:
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

		if e["repeat"] == 'Allday' or e["repeat"] == 2:
			monthName = date(1900, int(ex["date"]["month"]), 1).strftime('%B')
			description = f'{ex["date"]["day"]} {monthName} {ex["date"]["year"]} Every hours'

		if e["repeat"] == 'Daily' or e["repeat"] == 3:
			ampm = "AM"
			Hour12 = int(ex["time"]["hour"])
			Minute = f'{ex["time"]["minute"]}'
			if ex["time"]["minute"] < 10:
				Minute = f'0{Minute}'
			if ex["time"]["hour"] > 12:
				Hour12 = ex["time"]["hour"] - 12
				ampm = "PM"
			description = f'{ex["date"]["weekday"]}, {Hour12}:{Minute} {ampm}'

		if e["repeat"] == 'Monthly' or e["repeat"] == 4:
			description = f'Every {ex["date"]["day"]}'

		if e["repeat"] == 'Yearly' or e["repeat"] == 5:
			monthName = date(1900, int(ex["date"]["month"]), 1).strftime('%B')
			description = f'Every {ex["date"]["day"]} {monthName}'

		return description
	except Exception as er:
		logger.logs(f"Wrong format {str(er)}")
		logger.logs(f"execute:{e}")
		return None

def check_due(event):
	execute = json.loads(event['execute'])
	if event["repeat"] == "Once":
		if event["type"] == "Wish" or event["type"] == "Play":
			hour = execute["time"]["hour"]
			minute = execute["time"]["minute"]
		else:
			time = datetime.strptime(execute["time"],'%H:%M')
			hour = time.hour
			minute = time.minute
	elif event["repeat"] == "Allday":
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
	
	logger.logs(f'event:{event["name"]}, due:{duration}')
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
