

import os
from flask import request, jsonify
import json
from flask import Flask
from flask import send_from_directory
from flask import Flask, render_template
from db import *
from configs import *
from flask_socketio import SocketIO

static_file_dir = os.path.join( "/".join(os.path.realpath(__file__).split("/")[:-1]) + "/", "interface") + "/"
app = Flask(__name__, template_folder=static_file_dir)

app.config["SECRET_KEY"] = b'secret'

socketio = SocketIO(app)
database_object = None

@socketio.on("login")
def get_login(data):
	global database_object
	print(data)
	if(data["type"] == "login_profile"):
		for key, value in data["data"].items():
			data["data"][key] = "".join(value)
		database_object.insert_login(data["url"], json.dumps(data["data"]))

@app.route('/scope', methods = ['POST'])
def send_scope():
	return json.dumps(scope)

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
@app.route('/index.html', methods = ['GET'])
def index():
	return send_from_directory(static_file_dir, "index.html")


@app.route('/search', methods = ['GET'])
@app.route('/search.html', methods = ['GET'])
def search():
	global database_object
	data = []
	page = int(request.args.get("p", 0))
	query = request.args.get("q", "")
	response = database_object.custom_query(query, page)

	for x in response:
		data.append({
				"url":x[0]
			})
	search = []
	if(0 < page):
		search.append({
				"name":"back",
				"query":query,
				"value":(page - 1)
			})
	if(0 < len(response)):
		search.append({
			"name":"next",
			"query":query,
			"value":(page + 1)
		})
	return render_template('search.html', data=data, search=search)


@socketio.on("urls")
def check_block(url_list):
	global database_object
	parrent = url_list[0]
	for i in url_list:
		database_object.insert_url(i, parrent)

if __name__ == '__main__':
	database_object = database()
	socketio.run(app, port=5000, host= '0.0.0.0')


