#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, jsonify
from flask_login import current_user,LoginManager,login_user,logout_user,login_required
from models import db,User
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from dateutil.parser import parse # type: ignore
import common
import requests, json # type: ignore
import config

import logwriter,os

current_directory = os.getcwd()
logger = logwriter.writer(current_directory + "/logs/","gui",__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = '195de30e06e4040837afd882b4966398'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.app_context().push()
db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# register Blueprint
from kalendar import kalendar as kalendar_blueprint
app.register_blueprint(kalendar_blueprint)
from papar import papar as papar_blueprint
app.register_blueprint(papar_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/')
@login_required
def index():
	descriptions = []
	due_items = []
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	if not token:
		return redirect("/logout")
	try:
		response = requests.get(f'{config.api_endpoint}/api/event/user',headers={"x-access-tokens": token})
	except Exception as e:
		logger.logs(f"Error {str(e)}")
		return render_template("Index.html",events="",events_due="",user="",menu="own")
	
	if response.status_code == 200:
		data = response.json()
		event = data['data']
		for e in event:
			try:
				description = common.executeTranslate(e)
				descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
									"execute":description,"acknowledge":e["acknowledge"],"owner":e['created_by'],"type":e['type']})
				event_due = json.loads(common.check_due(e))
				if event_due['isDue']:
					due_items.append({"id":e['id'], "Name":e['name'], "Due":event_due['minutes']})
			except Exception as e:
				logger.logs("broken data at {}".format(e["id"]))
				pass
		eve = json.loads('{}')
		eve.update({"data":descriptions})
		events = eve["data"]
		events_due = json.dumps(due_items)
        #logger.logs(f"User:{current_user.username}")
		return render_template("Index.html",events=events,events_due=events_due,user=current_user,menu="own")
		
	if response.status_code == 404:
		return render_template("Index.html",events='',events_due="",user=current_user,menu="own")

	return render_template("Index.html",events='',events_due="",user=current_user,menu="own")

@app.route('/all')
@login_required
def all():
	descriptions = []
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	try:
		response = requests.get(f'{config.api_endpoint}/api/event',headers={"x-access-tokens": token})
	except Exception as e:
		logger.logs("Exception")
		return render_template("Index.html",events="",events_due="",user="",menu="all")

	if response.status_code == 200:
		data = response.json()
		event = data['data']
		for e in event:
			description = common.executeTranslate(e)
			descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
						"execute":description,"acknowledge":e["acknowledge"],"owner":e["created_by"],'type':e['type']})
		eve = json.loads('{}')
		eve.update({"data":descriptions})
		events = eve["data"]
		logger.logs(f"User:{current_user.username}")
		return render_template("Index.html",events=events,events_due="",user=current_user,menu="all")

	if response.status_code == 404:
		return render_template("Index.html",events='',events_due="",user=current_user,menu="all")

	return render_template("Index.html",events='',events_due="",user=current_user,menu="all")

@app.route('/detail')
@login_required
def detail():
	id = request.args.get('id')
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)

	response = requests.get(f'{config.api_endpoint}/api/event/id?id={id}', headers={"x-access-tokens": token})
	if response.status_code == 200:
		data = response.json()
		event = data["data"]
		createdBy = event["created_by"]
		for t in get_type()["data"]:
			if t["name"] == event["type"]:
				type = t["name"]
		for r in get_repeat()["data"]:
			if r["name"] == event["repeat"]:
				repeat = r["name"]
		created_by = createdBy
		description = common.executeTranslate(event)
		return render_template("Detail.html",event=event,execute=description, \
			type=type,repeat=repeat,created_by=created_by,error='')

	if response.status_code == 404:
		return render_template("Detail.html",event=event,execute=description, \
			type='',repeat='',created_by='',error=data['message'])

	return redirect("/")

@app.route('/today')
@login_required
def todayEvent():
	descriptions = []
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	weekdayName = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	today = datetime.now()
	weekday = weekdayName[today.weekday()]
	response = requests.get(f'{config.api_endpoint}/api/event', headers={"x-access-tokens": token})

	if response.status_code == 200:
		data = response.json()
		event = data['data']
		for e in event:
			try:
				ex = json.loads(e["execute"])
			except Exception as e:
				logger.logs(f'Error: {e}')
				continue

			if e["repeat"] == 'Once' \
				and today.day == ex["date"]["day"] \
				and today.month == ex["date"]["month"] \
				and today.year == ex["date"]["year"]:

				description = common.executeTranslate(e)
				descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
							"execute":description,"acknowledge":e["acknowledge"], \
							"owner":e["created_by"],"type":e["type"]})

			if e["repeat"] == 'Allday' \
				and today.day == ex["date"]["day"] \
				and today.month == ex["date"]["month"] \
				and today.year == ex["date"]["year"]:
				description = common.executeTranslate(e)
				descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
                                                 	"execute":description,"acknowledge":e["acknowledge"], \
							"owner":e["created_by"],"type":e["type"]})
			if e["repeat"] == 'Daily' \
			and ex["date"]["weekday"] == weekday:
				description = common.executeTranslate(e)
				descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
							"execute":description,"acknowledge":e["acknowledge"], \
							"owner":e["created_by"],"type":e["type"]})
			if e["repeat"] == 'Monthly' \
			and ex["date"]["day"] == today.day:
				description = common.executeTranslate(e)
				descriptions.append({"id":e["id"],"name":e["name"],"text":e["text"], \
							"execute":description,"acknowledge":e["acknowledge"], \
							"owner":e["created_by"],"type":e["type"]})
			if e["repeat"] == 'Yearly' \
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
		return render_template("Index.html",events=events,events_due="",user=current_user,menu="today")
	if response.status_code == 404:
		return render_template("Index.html",events='',events_due="",user=current_user,menu="today")
	return redirect("/")

@app.route('/update',methods=['POST'])
@login_required
def update():
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	user = get_login_user()
	id = request.form.get('id')
	name = request.form.get('name')
	text = request.form.get('text')
	type = request.form.get('type')
	repeat = request.form.get('repeat')
	execute = request.form.get('execute')
	parent = request.form.get('parent')
	int_type = common.get_type_id(type)
	int_repeat = common.get_repeat_id(repeat)
	#----Update change---#
	response = requests.put(f'{config.api_endpoint}/api/event', \
                                json={"id": int(id), "name": name,"text": text, \
                                "type": int_type,"repeat": int_repeat, \
                                "parent": int(parent),"execute": execute }, headers={"x-access-tokens": token})
	if response.status_code == 200:
		logger.logs("update success")
	else:
		logger.logs("Update failed")
	return redirect("/")

@app.route('/login',methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		if current_user.is_authenticated:
			return redirect("/")
		return render_template("Login.html",error='')

	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		isRemember = request.form.get('remember_me')
		try:
			user = User.query.filter_by(username=username).first()
		except Exception as e:
			logger.logs(f"Error: {str(e)}")
		if user and bcrypt.check_password_hash(user.password, password):
			if isRemember:
				login_user(user, remember=True, duration=timedelta(days=30))
			else:
				login_user(user)
			common.redis_client.set(str(current_user.publicId),password)
			return redirect('/')
		return render_template("Login.html",error='Invalid username or password')

@app.route('/logout')
def logout():
	common.clean_up(current_user.username,current_user.publicId)
	logout_user()
	return redirect('/login')

@app.route('/', methods=['POST'])
@login_required
def addItem():
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
	# logger.logs(f'Name:{name}\nText:{text}\nType:{type}\nRepeat:{repeat}\nMonth:{month}\nDay:{day}\n' \
	# 		+ f'DPicker:{datepicker}\nDTPicker:{datetimepicker}\nTPicker:{timepicker}\nWeekday:{weekday}')
	if type == '3': text = media
	if repeat == '1':
		add_once(name,text,type,repeat,datetimepicker)

	if repeat == '2':
		add_allday(name,text,type,repeat,datepicker)

	if repeat == '3':
		add_daily(name,text,type,repeat,timepicker,weekday)

	if repeat == '4':
		add_monthly(name,text,type,repeat,day)

	if repeat == '5':
		add_yearly(name,text,type,repeat,day,month)

	return redirect('/')

@app.route('/', methods=['DELETE'] )
@login_required
def deleteItem():
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	user = get_login_user()
	try:
		delete_id = request.args.get('id')
	except Exception as e:
		return jsonify({'error':str(e),'message':'Incorect value'}), 400

	response = requests.delete(f'{config.api_endpoint}/api/event?id={delete_id}', headers={"x-access-tokens": token})
	if response.status_code == 202:
		data = response.json()
		return jsonify({'message': delete_id +' was deleted'}), 202

	return jsonify({'message': 'Fail to delete'}), 400

def add_once(name,text,type,repeat,datetimepicker):
	#2024-03-19T20:38:43
	#strDateTime = parse(datetimepicker)
	#logger.logs(type(strDateTime).toString())
	#format = '%Y-%m-%d %H:%M:%S'
	#dt = datetime.strptime(strDateTime,format)
	dt = parse(datetimepicker)
	execute = '{"date":{"day":' + str(dt.day) + ',"month":' + str(dt.month) + ',"year":' + str(dt.year) + '}' \
			+ ',"time":{"hour":' + str(dt.hour) + ',"minute":' + str(dt.minute) + ',"second":' + str(dt.second) + '}}'
	# logger.logs(execute)
	store_event(name,text,type,repeat,0,execute)

def add_allday(name,text,type,repeat,datepicker):
	#2024-04-06
	#strDateTime = parse(datepicker)
	#logger.logs(strDateTime)
	#format = '%Y-%m-%d %H:%M:%S'
	d = parse(datepicker)
	execute = '{"date":{"day":' + str(d.day) + ',"month":' + str(d.month) + ',"year":' + str(d.year) + '}}'
	logger.logs(execute)
	store_event(name,text,type,repeat,0,execute)

def add_daily(name,text,type,repeat,timepicker,weekday):
	#13:44:06
	#strDateTime = parse(timepicker)
	#logger.logs(strDateTime)
	isFirst = True
	parent = 0
	#format = '%Y-%m-%d %H:%M:%S'
	t = parse(timepicker)
	for w in weekday:
		execute = '{"date":{"weekday":"' + w + '"},"time":{"hour":' + str(t.hour) + ',"minute":' + str(t.minute) + ',"second":' + str(t.second) + '}}'
		logger.logs(execute)
		if isFirst:
			isFirst = False
			parent = store_event(name,text,type,repeat,0,execute)
		else:
			if not parent == 0:
				store_event(name,text,type,repeat,parent,execute)
			else:
				logger.logs("daily store fail")
def add_monthly(name,text,type,repeat,day):
	execute = '{"date":{"day":' + day + '}}'
	logger.logs(execute)
	store_event(name,text,type,repeat,0,execute)

def add_yearly(name,text,type,repeat,day,month):
	execute = '{"date":{"day":' + day + ',"month":' + month + '}}'
	logger.logs(execute)
	store_event(name,text,type,repeat,0,execute)

def store_event(name,text,type,repeat,parent,execute):
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	#--start send data to store--

	url = f'{config.api_endpoint}/api/event'

	headers={'Content-Type' : 'application/json', \
                 'x-access-tokens' : token }

	response = requests.post(url, json={"name": name,"text": text, \
                		"type": type,"repeat": repeat, \
                		"parent": parent,"execute": execute },
				headers=headers)

	if response.status_code == 201:
		data = response.json()
		id = data['data']['id']
		#--update parent if not have parent--

		if data["data"]["parent"] == 0:
			update = requests.put(f'{config.api_endpoint}/api/event/parent', \
					json={"id":id,"parent": id}, headers={"x-access-tokens": token})
			update_data = update.json()
			if update.status_code == 202:
				logger.logs("event store success")
				return update_data['data']['id']

			else:
				message = update_data['message']

				if 'error' in update_data:
					message  += ', ' +  update_data['error']
				logger.logs(f'event update fail error:{message}')

	else:
		logger.logs("event store request fail")

	if response.status_code == 403 or response.status_code == 400:
		return redirect("/login")

	return None

def get_login_user():
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	response = requests.post(f'{config.api_endpoint}/api/user_info', headers={"x-access-tokens": token})
	data = response.json()
	if response.status_code == 200:
		user = data['data']
		return user
	if response.status_code ==  403 or response.status_code ==  400:
		return redirect("/login")

	logger.logs(f'response{response.status_code}')
	return None

@app.route('/account', methods=['POST'])
@login_required
def add_user():
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	username = request.form.get("username")
	email = request.form.get("email")
	password = request.form.get("password")
	logger.logs(f'Username: {username}, Email: {email}, Password: {password}')
	response = requests.post(f'{config.api_endpoint}/api/users', \
				json={"username": username,"password": password,"email": email, 'isAdmin': False}, headers={"x-access-tokens": token})
	if response.status_code == 201:
		data = response.json()
	else:
		logger.logs("Fail to add user")

	return redirect("/")

@app.route('/changepassword', methods=['POST'])
@login_required
def change_password():
	try:
		record = json.loads(request.data)
	except Exception as e:
		return jsonify({'message':'missing parameter', 'error':str(e)}), 400

	user = User.query.filter_by(id=current_user.id).first()

	if user and bcrypt.check_password_hash(user.password, record['password']):
		hashed_password = bcrypt.generate_password_hash(record['new-password']).decode('utf-8')
		user.password = hashed_password
		db.session.commit()

		return jsonify({'message':'password updated!'}), 202

	return jsonify({'message':'Wrong password!','error': None}), 403

@app.route('/gettype', methods=['GET'] )
@login_required
def get_type():
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	response = requests.get(f'{config.api_endpoint}/api/event/type', headers={"x-access-tokens": token})
	if response.status_code == 200:
		data = response.json()
		return data
	return jsonify({"message":"fail connect to api service"}), 500
@app.route('/getrepeat', methods=['GET'] )
@login_required
def get_repeat():
	token = common.get_token(username=current_user.username,publicId=current_user.publicId)
	response = requests.get(f'{config.api_endpoint}/api/event/repeat', headers={"x-access-tokens": token})
	if response.status_code == 200:
		data = response.json()
		return data
	return jsonify({"message":"fail connect to api service"}), 500

@app.route('/getmedia', methods=['GET'] )
@login_required
def get_media():
	response = requests.get(f'{config.spoke_endpoint}/audio_list')
	if response.status_code == 200:
		data = response.json()
		return data
	return jsonify({"message":"fail connect to spoke service"}), 500

if __name__ == '__main__':
	from waitress import serve # type: ignore
	serve(app, host="0.0.0.0", port=5000)
        #app.run(host='0.0.0.0', port =5000, debug=False)
