from flask import jsonify
from flask_login import current_user
import config
import requests, json # type: ignore
import logging
from datetime import datetime, date, timedelta
import redis


redis_client = redis.Redis(host=config.redis_host, port=config.redis_port, db=0)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def refresh_token(username,publicId):
	password = redis_client.get(str(publicId))
	if not password:
		logger.error("password is empty")
	response = requests.post(f'{config.api_endpoint}/api/login', auth = (username, password))
	if response.status_code == 200:
		data = response.json()
		token = data['token']
		redis_client.set(username,token)
		data = redis_client.get(username)
		return data
	else:
		logger.error(f"Fail to login {username} to api")
	return None

def get_token(username,publicId):
	data = redis_client.get(username)
	if not data:
		logger.error("uername is empty")
	token = handle_token(token=data,username=username,publicId=publicId)
	if not token:
		token = refresh_token(username=username,publicId=publicId)
	return token

def handle_token(token,username,publicId):
	response = requests.get(f'{config.api_endpoint}/api/user_info',headers={"x-access-tokens": token})
	if response.status_code == 403:
		data = response.json()
		if data['error'] == 'Signature has expired':
			newToken = refresh_token(username=username,publicId=publicId)
			return newToken
	return token

def clean_up(username,publicId):
	redis_client.delete(username)
	redis_client.delete(str(publicId))

def executeTranslate(e):
	try:
		ex = json.loads(e['execute'])
	except Exception as er:
		logger.error(f"Wrong format {str(er)}")
		logger.info(f"execute:{e}")

	if e["repeat"] == 'Once' or e["repeat"] == 1:
		monthName = date(1900, int(ex["date"]["month"]), 1).strftime('%B')
		ampm = "AM"
		if e["type"] == "Prayer" or e["type"] == 2:
			time = datetime.strptime(ex["time"],'%HH:%MM')
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
	time_diff = event_datetime - datetime.now()
	minutes = time_diff.total_seconds() / 60 
	if minutes < 1.0 :
		return json.dumps({'isDue': True,'minutes': abs(int(minutes))})
	return json.dumps({'isDue': False,'minutes': abs(int(minutes))})

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

def get_type_id(name: str):
	token = get_token(username=current_user.username,publicId=current_user.publicId)
	response = requests.get(f'{config.api_endpoint}/api/event/type', headers={"x-access-tokens": token})
	if response.status_code == 200:
		all_data = response.json()
		for d in all_data["data"]:
			if d['name'] == name :
				return d['id']
		logger.error(f"Name of type {name} not found")
	logger.error(f"request no success")
	return None

def get_repeat_id(name: str):
	token = get_token(username=current_user.username,publicId=current_user.publicId)
	response = requests.get(f'{config.api_endpoint}/api/event/repeat', headers={"x-access-tokens": token})
	if response.status_code == 200:
		all_data = response.json()
		for d in all_data["data"]:
			if d['name'] == name :
				return d['id']
		logger.error(f"Name of repeat {name} not found")
	logger.error(f"request no success")
	return None