import sqlite3
from flask import *
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/logsig', methods=['POST'])
def logsig():
	print(request.form)
	if 'login' in request.form:
		return ('login')
	return 'signup'

#with app.test_request_context():
#	print(url_for('static', filename='css/style.css'))
app.run(host='0.0.0.0', port=8888)
