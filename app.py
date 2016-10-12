import requests
from flask import Flask, request, json, jsonify, Response
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>VGMDB tools</h1>'

@app.route('/album')
def album():
	return '<h1>VGMDB tools</h1><h2>Album</h2><form action="/album-search" method="POST"><label>URL: </label><input type="text" name="albuminput"><input type="submit" value="Submit"></input></form>'

@app.route('/album-search', methods = [ 'POST' ])
def album_search():
	album_input = request.form['albuminput']
	tokens = album_input.split("/")
	for i in tokens:
		if i.isdigit():
			album_id = i
			r = requests.get('http://vgmdb.info/album/' + album_id + '?format=json')
			if r.status_code==200:
				return Response(response=r, status=200, mimetype='application/json', content_type='application/json, charset=utf-8')
			else:
				resp = r.text
				return resp
	return 'ERROR: album not found'

if __name__ == '__main__':
	application.run(host='0.0.0.0')

