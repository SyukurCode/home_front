#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from datetime import datetime
from flask_bcrypt import Bcrypt
from apirequest import get_response, put_response, \
	delete_response, post_response, get_response_spoke, get_user_avatar
import requests, json, config,logwriter,os,common,csv
from werkzeug.utils import secure_filename
from model import index_model, detail_model, login_model, notification_model

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = '195de30e06e4040837afd882b4966398'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.app_context().push()

bcrypt = Bcrypt(app)


# register Blueprint
from kalendar import kalendar as kalendar_blueprint
app.register_blueprint(kalendar_blueprint)
from papar import papar as papar_blueprint
app.register_blueprint(papar_blueprint)
from maps import maps as maps_blueprint
app.register_blueprint(maps_blueprint)
from waktusolat import waktu_solat as waktusolat_blueprint
app.register_blueprint(waktusolat_blueprint)

@app.route('/')
def index():
	descriptions = []
	current_user = common.session_get('User')
	response = get_response('/api/event/user')

	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data')
		return render_template("Login.html", **error_msg)
 
	event = response['data']
	for e in event:
		description = common.executeTranslate(e)
		descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
							"execute":description,"acknowledge":e["acknowledge"],"owner":e['created_by'],"type":e['type']})
		
	eve = json.loads('{}')
	eve.update({"data":descriptions})
	events = eve["data"]
	viewdata = index_model(events=events, user=current_user, avatar=get_user_avatar() \
						 if get_user_avatar() else None, menu="own").to_dict()
	return render_template("Index.html", **viewdata)

@app.route('/all')
def all():
	descriptions = []
	current_user = common.session_get("User")
	response = get_response('/api/event')

	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data')
		return render_template("Login.html", **error_msg)
 
	event = response['data']
	for e in event:
		description = common.executeTranslate(e)
		descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
					"execute":description,"acknowledge":e["acknowledge"],"owner":e["created_by"],'type':e['type']})
	eve = json.loads('{}')
	eve.update({"data":descriptions})
	events = eve["data"]

	viewdata = index_model(events=events, user=current_user, avatar=get_user_avatar() \
						 if get_user_avatar() else None, menu="all").to_dict()
	return render_template("Index.html",**viewdata)
	
@app.route('/detail')
def detail():
	id = request.args.get('id')
	current_user = common.session_get("User")
	response = get_response(f'/api/event/id?id={id}')

	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data')
		return render_template("Login.html", **error_msg)
 
	event = response['data']
	description = common.executeTranslate(event)

	viewdata = detail_model(event=event, user=current_user, \
							avatar=get_user_avatar() if get_user_avatar() else None, \
							execute=description).to_dict()
	return render_template("Detail.html", **viewdata)


@app.route('/today')
def todayEvent():
	descriptions = []
	current_user = common.session_get("User")
	weekdayName = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	today = datetime.now()
	weekday = weekdayName[today.weekday()]
	response = get_response('/api/event')

	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data')
		return render_template("Login.html", **error_msg)
 
	event = response['data']
	for e in event:
		try:
			ex = json.loads(e["execute"])
		except Exception as e:
			logger.logs(f'Error: {e}')
			continue

		if e["event_repeat"]["name"] == 'Once' \
			and today.day == ex["date"]["day"] \
			and today.month == ex["date"]["month"] \
			and today.year == ex["date"]["year"]:

			description = common.executeTranslate(e)
			descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
						"execute":description,"acknowledge":e["acknowledge"], \
						"owner":e["created_by"],"type":e["type"]})

		if e["event_repeat"]["name"] == 'Allday' \
			and today.day == ex["date"]["day"] \
			and today.month == ex["date"]["month"] \
			and today.year == ex["date"]["year"]:
			description = common.executeTranslate(e)
			descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
												"execute":description,"acknowledge":e["acknowledge"], \
						"owner":e["created_by"],"type":e["type"]})
		if e["event_repeat"]["name"] == 'Daily' \
		and ex["date"]["weekday"] == weekday:
			description = common.executeTranslate(e)
			descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
						"execute":description,"acknowledge":e["acknowledge"], \
						"owner":e["created_by"],"type":e["type"]})
		if e["event_repeat"]["name"] == 'Monthly' \
		and ex["date"]["day"] == today.day:
			description = common.executeTranslate(e)
			descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
						"execute":description,"acknowledge":e["acknowledge"], \
						"owner":e["created_by"],"type":e["type"]})
		if e["event_repeat"]["name"] == 'Yearly' \
		and ex["date"]["day"] == today.day \
		and ex["date"]["month"] == today.month:
			description = common.executeTranslate(e)
			descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
						"execute":description,"acknowledge":e["acknowledge"], \
						"owner":e["created_by"],"type":e["type"]})
		#logger.logs(f'{ex["date"]["day"}:{today.day},{ex["date"]["month"]}:{today.month}')
		eve = json.loads('{}')
		eve.update({"data":descriptions})
		events = eve["data"]

	viewdata = index_model(events=events, user=current_user, \
							avatar=get_user_avatar() if get_user_avatar() else None, \
							menu="today").to_dict()
	
	return render_template("Index.html",**viewdata)

@app.route('/update',methods=['POST'])
def update():
	current_user = common.session_get("User")
	id = request.form.get('id')
	name = request.form.get('name')
	text = request.form.get('text')
	type = request.form.get('type')
	repeat = request.form.get('repeat')
	execute = request.form.get('execute')
	parent = request.form.get('parent')
	int_type = int(type)
	int_repeat = int(repeat)

	response = put_response(f'/api/event', \
							{"id": int(id), "name": name,"text": text, \
							"type": int_type,"repeat": int_repeat, \
							"parent": int(parent),"execute": execute })
	
	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data')
		return render_template("Login.html", **error_msg)
	
	return redirect("/")


@app.route('/login',methods=['GET', 'POST'])
def login():
	token = common.session_get("Token")
	if request.method == 'GET':
		if token:
			return redirect("/")
		viewdata = {
			"error": '',
			"username": session.get('username', ''),
			"password": session.get('password', ''),
		}
		return render_template("Login.html", **viewdata)
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		isRemember = request.form.get('remember_me')
		
		if isRemember:
			session.permanent = True  # Makes the session permanent
		else:
			session.permanent = False  # Makes the session temporary
		
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
				viewdata = login_model(session_data=session, error=data['detail'])
				return render_template("Login.html", **viewdata.to_dict())
			
			
			token = data['access_token']
			session['Token'] = token

			response = get_response('/api/user_info')

			if not isinstance(response, dict) or response.get('status_code') != 200:
				error_msg = response.get('data')
				return render_template("Login.html", **error_msg)

			session['User'] = response['data']
			session['username'] = username
			session['password'] = password
			session['remember'] = isRemember
			return redirect("/")

		except requests.exceptions.RequestException as e:
			viewdata = {
				"error": str(e),
				"username": session.get('username', ''),
				"password": session.get('password', ''),
				"remember": session.get('remember', False),
			}
			return render_template("Login.html",**viewdata)
		
@app.route('/logout')
def logout():
	session.clear()
	return redirect('/login')

@app.route('/', methods=['POST'])
def addItem():
	token = common.session_get("Token")
	if not token:
		return redirect("/logout")
	
	name = request.form.get('ename')
	text = request.form.get('etext')
	media = request.form.get('media')
	type = request.form.get('type')
	repeat = request.form.get('repeat')
	month = request.form.get('emonth')
	day = request.form.get('eday')
	datepicker = request.form.get('datepicker')
	datetimepicker = request.form.get('datetimepicker')
	timepicker = request.form.get('timepicker')
	weekday = request.form.getlist('weekday')
 
	if type == '3': text = media
	if repeat == '1':
		common.add_once(name,text,type,repeat,datetimepicker)

	if repeat == '2':
		common.add_allday(name,text,type,repeat,datepicker)

	if repeat == '3':
		common.add_daily(name,text,type,repeat,timepicker,weekday)

	if repeat == '4':
		common.add_monthly(name,text,type,repeat,day)

	if repeat == '5':
		common.add_yearly(name,text,type,repeat,day,month)

	return redirect('/')

@app.route('/', methods=['DELETE'] )
def deleteItem():
	token = common.session_get("Token")
	current_user = common.session_get("User")

	if not token:
		return redirect("/logout")
	
	try:
		delete_id = request.args.get('id')
	except Exception as e:
		return jsonify({'error':str(e),'message':'Incorect value'}), 400

	response = delete_response(f'/api/event?id={delete_id}')
	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data', 'Unknown error')
		return jsonify({"error": error_msg})
	
	return jsonify({'message': delete_id +' was deleted'}), 202

@app.route('/account', methods=['POST'])
def add_user():
	username = request.form.get("username")
	email = request.form.get("email")
	password = request.form.get("password")

	logger.logs(f'Username: {username}, Email: {email}, Password: {password}')

	response = post_response('/api/users', \
							{"username": username,"password": password,"email": email, 'isAdmin': False})
	
	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data', 'Unknown error')
		return render_template("Login.html", **error_msg)
	
	data = response['data']
	
	return redirect("/")

@app.route('/changepassword', methods=['POST'])
def change_password():
	current_user = common.session_get("User")
	try:
		record = json.loads(request.data)
	except Exception as e:
		return jsonify({'message':'missing parameter', 'error':str(e)}), 400

	isValid = common.get_token(record['username'],record['password'])
	if not isValid == None:
		userId = current_user['id']
		response = put_response(f'/api/user/{userId}', \
							{"password": record['new-password'], \
							"email": current_user['email'],"isAdmin": current_user['isAdmin']})
		
		if not isinstance(response, dict) or response.get('status_code') != 200:
			error_msg = response.get('data', 'Unknown error')
			return jsonify({"error": error_msg}), response.get('status_code', 500)

		data = response['data']
            
		return jsonify({'message':'password updated!'}), 202
	return jsonify({'message':'Wrong password!','error': None}), 403

@app.route('/gettype', methods=['GET'] )
def get_type():
	response = get_response('/api/event/type')
	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data', 'Unknown error')
		return jsonify({"error":error_msg})
	data = response['data']	
	
	return data
	

@app.route('/getrepeat', methods=['GET'] )
def get_repeat():
	response = get_response('/api/event/repeat')
	
	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data', 'Unknown error')
		return jsonify({"error":error_msg}), 500

	data = response['data']
	return data

@app.route('/getmedia', methods=['GET'] )
def get_media():

	response = get_response_spoke('/audio_list')
	if not isinstance(response, dict) or response.get('status_code') != 200:
		error_msg = response.get('data', 'Unknown error')
		return jsonify({"message":error_msg}), 500

	data = response['data']
	return data

@app.route('/checkeventdue', methods=['GET'])
def due_event():
	token = common.session_get("Token")
	due_items = []

	response = get_response('/api/event/user')

	data = response['data']
	event = data
	for e in event:
		event_due = json.loads(common.check_due(e))
		if event_due['isDue']:
			due_items.append({"id":e['id'], "Name":e['name'], "Due":event_due['duration']})
	events_due = json.dumps(due_items)
	return jsonify(events_due),200

@app.route('/notifications', methods=['GET'])
def notification():
    current_user = common.session_get("User")
    response = get_response('/api/event/user')
    
    data = response['data']
    due_items = []
    for e in data:
        event_due = json.loads(common.check_due(e))
        if event_due['isDue']:
            due_items.append({"id": e['id'], "Name": e['name'], "Due": event_due['duration']})
            
    viewdata = notification_model(events=due_items,	user=current_user,avatar=get_user_avatar() if get_user_avatar() else None
	).to_dict()
	
    return render_template("Notification.html", **viewdata)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
	current_user = common.session_get("User")
	error = ''
	if 'csvFile' not in request.files:
		return jsonify({'error': 'No file part'}), 400
		 
	file = request.files['csvFile']

	if file and file.filename.endswith('.csv'):
		csv_data = []
		stream = file.stream.read().decode("utf-8").splitlines()
		reader = csv.reader(stream)
		next(reader, None)  # Skip the header row
		for row in reader:
			
			try:
				event_date = datetime.strptime(row[0], '%d/%m/%Y')
				event_time = datetime.strptime(row[1], '%H:%M')
				event_datetime = datetime.strptime(f"{row[0]} {row[1]}", "%d/%m/%Y %H:%M")
			except ValueError as e:
				logger.logs(f"Error parsing date: {e}")
				csv_data.append({"event" : row, "error": e, "status": "Fail" })
				continue
				
			name = row[2]
			text = row[3]
			type = row[4] #wish
			repeat = row[5] #allday
			parent = 0 #individual
			
			try:
				if repeat == '1' and type == '1': #once and wish
					response = common.add_once(name=name,text=text,type=type,repeat=repeat,datetimepicker=event_datetime.strftime('%Y-%m-%d %H:%M:%S'))
				if repeat == '2' and type == '1': #allday and wish
					response = common.add_allday(name=name,text=text,type=type,repeat=repeat,datepicker=event_date.strftime('%Y-%m-%d'))
				
				if response["status"] != "success":
					logger.logs(f'Error: {response["message"]}')
					csv_data.append({"event" : row, "error": response["message"], "status": "fail" })
				
				csv_data.append({"event" : row, "error": "", "status": "Pass" })
				logger.logs(f"Event stored: {name}, {text}, {type}, {repeat}, {parent}")

			except Exception as e:
				logger.logs(f"Error storing event: {e}")
				csv_data.append({"event" : row, "error": e, "status": "Fail" })
				continue
		
	else:
		return jsonify({'error': 'Invalid file format'}), 400
		
	if file.filename == '':
		return jsonify({'error': 'No selected file'}), 400
	
	viewdata = {
		"items" : csv_data,
		"user" : current_user,
        "avatar" : get_user_avatar() if get_user_avatar() else None,
	}

	return render_template("EventUpload.html", **viewdata)


@app.route('/upload-avatar', methods=['POST'])
def upload_avatar():
	token = common.session_get("Token")
	file = request.files.get('avatar')
	if not file:
		return jsonify({"detail": "No file uploaded"}), 400
	
	filename = secure_filename(file.filename)

	files = {
        'file': (filename, file.stream, file.mimetype)
    }
    
	headers={"Authorization":f"Bearer {token}"}

	response = requests.post(f'{config.api_endpoint}/api/avatar', files=files, headers=headers)
    
	if response.status_code != 200:
		try:
			error_msg = response.json()['detail']	
		except ValueError:
			error_msg = 'Invalid response format'
		return jsonify({"detail": error_msg}), 500
    
	if response.status_code == 200:
		avatar = get_user_avatar()
		return jsonify({'data': avatar}), 200
	

# on error 404
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
	
if __name__ == '__main__':
	# from waitress import serve # type: ignore
	# serve(app, host="0.0.0.0", port=5000)
	app.run(host='0.0.0.0', port =5000, debug=True)
