from app import app, WEB_API, bbc_crawler
from flask import jsonify
from flask_cors import CORS

app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)


@app.route('/')
def index():
    return jsonify({'news': WEB_API.get_newslist('BBC', 1)}), 200, {"function": "getNews"}

@app.route('/bbc')
def bbc():
    result = bbc_crawler.bbc_crawler()
    return result, 200, {"function": "bbc"}

@app.route('/newsBitcoin')
def newsBitcoin():
    return jsonify({'news': 'newsBitcoin'}), 200, {"function": "getNews"}
