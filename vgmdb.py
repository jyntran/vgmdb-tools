import requests
from flask import Flask, request, json, jsonify, Response, render_template, flash
app = Flask(__name__)

@app.route('/')
def index():
        links = [
            { 'title': 'Album Tagging Tool',
              'url': '/album',
              'description': 'Gives basic information about VGMDB albums in an easy-to-copypasta way to make tagging easier'
            }
        ]
        return render_template('nav.html', links=links)

@app.route('/album')
def album():
        return render_template('album_tagging.html')

@app.route('/album-search', methods = [ 'POST' ])
def album_search():
	album_input = request.form['albuminput']
	tokens = album_input.split("/")
	for i in tokens:
		if i.isdigit():
			album_id = i
			r = requests.get('http://vgmdb.info/album/' + album_id + '?format=json')
			if r.status_code==200:
                                flash('Success')
				return Response(response=r, status=200, mimetype='application/json', content_type='application/json', charset='utf-8')
			else:
				resp = r.text
                                flash('Error')
				return resp
        flash('Error')
	return 'ERROR: album not found'

@app.route('/album-tagging', methods = [ 'POST' ])
def album_tagging():
        data = None
        info = {}
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
                info['name'] = data['name']
		if data['names']:
                        info['names'] = data['names']
                if data['link']:
                        info['link'] = 'http://vgmdb.net/' +  data['link']

                # get artists
                if data['composers']:
                        info['composers'] = []
                        for c in data['composers']:
                                info['composers'].append(c['names'])
                if data['performers']:
                        info['performers'] = []
                        for p in data['performers']:
                                info['performers'].append(p['names'])
                if data['lyricists']:
                        info['lyricists'] = []
                        for l in data['lyricists']:
                                info['lyricists'].append(l['names'])
                if data['arrangers']:
                        info['arrangers'] = []
                        for a in data['arrangers']:
                                info['arrangers'].append(a['names'])

		# get cover art
		if data['covers']:
			for c in data['covers']:
                                info['cover'] = data['covers'][0]['full']

		# get all languages and tracks
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
                info['tracklist'] = tracks

                # get notes
                if data['notes']:
                    info['notes'] = data['notes']

		return render_template('album_tagging_result.html', data=info)
	else:
                error = "Error: album not found"
		return render_template('album_tagging_result.html', error=error)

if __name__ == '__main__':
	app.run()
#	application.run(host='0.0.0.0')

