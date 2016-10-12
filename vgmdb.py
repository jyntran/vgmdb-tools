from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
	return "<h1>VGMDB tools</h1>"

if __name__ == "__main__":
	application.run(host='0.0.0.0')

