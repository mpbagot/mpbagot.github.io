import db
from flask import *
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/logsig', methods=['POST'])
def logsig():
	if 'login' in request.form:
		return render_template('logsig_template.html', login=True, title="Login")
	return render_template('logsig_template.html', login=False, title="Sign-Up")

@app.route('/<pagename>')
def content_handler(pagename):
	pagename = pagename.split('.')[0]
	dc = {'pacrpg':'Pepper & Carrot RPG', 'ghssound':'GHS Soundboard', 'blog':'SDD Design Subsite'}
	return render_template('content_template.html', title=dc[pagename])

app.run(host='0.0.0.0', port=8888, threaded=True)
