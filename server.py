from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/data")
def data():
	d = json.load(open('data.json', 'r'))
	return jsonify(d)

if __name__ == '__main__':
	app.run(debug=True)