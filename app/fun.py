import os
from flask import jsonify
from app.WEB_API import *
from app.crawler import *

backend_SERVERURL = os.getenv('Heroku_backend')


def bbc_crawler():
    last_date=get_lastNews_datetime('BBC')
    newslist = (get_bbc_news(last_date))
    result = post_newslist(newslist) if len(newslist) > 0 else jsonify({"result": "no new news"})
    return result
def get_lastNews_datetime(news_website):
    last_news = get_newslist(news_website, 1)
    return last_news['data']['news'][0]['news_datetime']
