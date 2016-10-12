from flask import Flask, request, json, jsonify
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>VGMDB tools</h1>'

@app.route('/album')
def album():
	return '<h1>VGMDB tools</h1><h2>Album</h2>'

@app.route('/album-search', methods = [ 'POST' ])
def album_search():
	if request.headers['Content-Type'] == 'text/plain':
		return "Text Message: " + request.data
	else:
		return "415 Unsupported Media Type"
	
if __name__ == '__main__':
	application.run(host='0.0.0.0')

