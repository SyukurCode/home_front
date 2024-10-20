import os
import config
import requests, json # type: ignore
import logging
from datetime import datetime, date, timedelta
import redis

endpoint = os.environ['API_HOST']
api_port = os.environ['API_PORT']
redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
endpoint = os.environ['API_HOST']
api_port = os.environ['API_PORT']

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def refresh_token(username,publicId):
	password = redis_client.get(str(publicId))
	response = requests.post(f'http://{endpoint}:{api_port}/api/login', auth = (username, password))
	if response.status_code == 200:
		data = response.json()
		token = data['token']
		redis_client.set(username,token)
		data = redis_client.get(username)
		return data
	return None

def get_token(username,publicId):
	data = redis_client.get(username)
	if not data:
		data = refresh_token(username=username,publicId=publicId)
	return data

def clean_up(username,publicId):
	redis_client.delete(username)
	redis_client.delete(str(publicId))

def executeTranslate(e):
	try:
		ex = json.loads(e['execute'])
	except Exception as e:
		return "Wrong format"
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
