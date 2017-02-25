#!/usr/bin/env python3
from flask import *

app = Flask(__name__)

@app.route('/')
def main():
    return open('index.html').read()

app.run(host='0.0.0.0', port=80, threaded=True)
