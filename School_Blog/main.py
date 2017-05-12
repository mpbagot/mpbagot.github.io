#!/usr/bin/env python3

from db import *
from flask import *
app = Flask(__name__)
app.jinja_env.autoescape = False

@app.route('/')
def index_handler():
	t = Topic.get_main_page()
	return render_template('index.html', topics=t, topic1=t[0], topic2=t[1], topic3=t[2])

@app.route('/add', methods=["POST","GET"])
def add_post_handler():
	form = request.form
	if request.method == "POST":
		pswd = form['pass']
		if pswd != "RandomPassHere":
			return render_template('add_post.html')
		topic = form['topic']
		date = form['date']
		title = form['title']
		text = form['main_text']
		post = Log(text, title, "None", int(topic), date=date)
		post.add()
		return index_handler()
	return render_template('add_post.html')

@app.route('/post/<post_id>')
def post_handler(post_id):
	post = Log.get(post_id)
	if not post:
		return render_template('404.html')
	topic = post.get_topic()
	# print('post_handler', topic, post)
	return render_template('post_template.html', title=post.title, post=post, topic=topic, topics=Topic.get_main_page())

@app.route('/topic/<topic_id>')
def topic_handler(topic_id):
	topic = Topic.get(topic_id)
	posts = Log.get_all(topic_id)
	# print('content_handler', topic, posts[0].id)
	return render_template('topic_template.html', title=topic.title+': '+topic.subtitle, posts=posts, topic=topic, topics=Topic.get_main_page())

app.run(host='0.0.0.0', port=3030)#, threaded=True)
