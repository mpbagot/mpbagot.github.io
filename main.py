from db import *
from flask import *
app = Flask(__name__)

def logged_in(request):
	return bool(request.cookies.get('user_id'))

@app.route('/')
def index():
	return render_template('index.html', logged_in=logged_in(request))

@app.route('/logsig', methods=['POST'])
def logsig():
	if 'username' in request.form and request.form['username'] != '':
		if 'confirm_password' in request.form:
			passwd = request.form['password']
			conf_passwd = request.form['confirm_password']
			if not passwd == conf_passwd:
				return render_template('logsig_template.html', logged_in=False, error="Passwords do not match!", login=False)
				# error with invalid input
			uname = request.form['username']
			u = User.get(uname=uname)
			if u:
				return render_template('logsig_template.html', logged_in=False, error="User already exists!", login=False)
				# user already exists
			u = User(uname, passwd)
			u.add()
			resp = make_response(render_template('index.html', logged_in=True))
			resp.set_cookie('user_id', '{}'.format(u.id))
			return resp
			# set a cookie with u.id
		else:
			uname = request.form['username']
			passwd = request.form['password']
			u = User.get(uname=uname)
			if u and u.password == passwd:
				# log them in with a cookie.
				resp = make_response(render_template('index.html', logged_in=True))
				resp.set_cookie('user_id', '{}'.format(u.id))
				print('Signing Up...')
				return resp
			elif u is None:
				return render_template('logsig_template.html', logged_in=False, error="User not found!", login=True)
				# username is bad
			else:
				return render_template('logsig_template.html', logged_in=False, error="Incorrect password!", login=True)
				# Password is bad
	elif 'logout' in request.form:
		resp = make_response(render_template('index.html', logged_in=False))
		resp.set_cookie('user_id', '', expires=0)
		print('Logging out...')
		return resp

	elif 'login' in request.form:
		return render_template('logsig_template.html', logged_in=False, login=True, title="Login")
	return render_template('logsig_template.html', logged_in=False, login=False, title="Sign-Up")

@app.route('/<pagename>')
def content_handler(pagename):
	pagename = pagename.split('.')[0]
	dc = {'pacrpg':'Pepper & Carrot RPG', 'ghssound':'GHS Soundboard', 'proj3_STANDIN':'Project 3'}
	return render_template('content_template.html', logged_in=logged_in(request), title=dc[pagename])

app.run(host='0.0.0.0', port=6657)#, threaded=True)
