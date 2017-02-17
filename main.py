import sqlite3
from flask import *
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

app.run(port=8888)
