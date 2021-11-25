from app import app, WEB_API
from flask import jsonify
from flask_cors import CORS

app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)


@app.route('/')
def index():
    return jsonify({'news': WEB_API.get_newslist('BBC', 1)}), 200, {"function": "getNews"}

@app.route('/bbc')
def bbc():
    return jsonify({'news': 'bbc'}), 200, {"function": "getNews"}

@app.route('/newsBitcoin')
def newsBitcoin():
    return jsonify({'news': 'newsBitcoin'}), 200, {"function": "getNews"}
