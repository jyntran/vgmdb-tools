import requests
from flask import Flask, request, json, jsonify, Response
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>VGMDB tools</h1>'

@app.route('/album')
def album():
	return '<h1>VGMDB tools</h1><h2>Album</h2><form action="/album-tracks" method="POST"><label>URL: </label><input type="text" name="albuminput"><input type="submit" value="Submit"></input></form>'

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

@app.route('/album-tracks', methods = [ 'POST' ])
def album_tracks():
	album_input = request.form['albuminput']
	tokens = album_input.split("/")
	for i in tokens:
		if i.isdigit():
			album_id = i
			r = requests.get('http://vgmdb.info/album/' + album_id + '?format=json')
			if r.status_code==200:
				data = json.loads(r.text) # dict
			else:
				resp = r.text
				return resp
	if data is not None:
		# get cover art
		cover = ''
		if data['covers']:
			for c in data['covers']:
				if c['name']=='Front':
					cover = c['full']

		# get all languages
		discs = data['discs']
		track = discs[0]['tracks'][0]
		languages = track['names']

		tracks = {}
		for l in languages:
			tracks[l] = {'l':[], 't':''}
			for d in data['discs']:
				for t in d['tracks']:
					tracks[l]['l'].append(t['names'][l])
					tracks[l]['t'] = tracks[l]['t'] + t['names'][l] + '\n'
		result = '<h1>Album Tracklist</h1><h2>' + data['name'] + '</h2>'
		for l in languages:
			result = result + '<h3>' + l + '</h3><textarea>' + tracks[l]['t'] + '</textarea>'
		if cover:
			result = result + '<h2>Cover Art</h2><img src="' + cover + '"/>'
		return result
	else:
		return 'ERROR: album not found'

if __name__ == '__main__':
	application.run(host='0.0.0.0')

