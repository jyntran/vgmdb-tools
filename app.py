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
				resp = Response(response=r, status=200, mimetype='application/json')
			else:
				resp = r.text
			return resp
	return 'ERROR: album not found'

@app.route('/album-result')
def album_result():
	return

#	if request.headers['Content-Type'] == 'text/plain':
#		return "Text Message: " + request.data
#	else:
#		return "415 Unsupported Media Type"
	
if __name__ == '__main__':
	application.run(host='0.0.0.0')

