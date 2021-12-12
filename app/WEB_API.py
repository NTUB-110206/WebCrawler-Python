import os
import requests
import json

backend_SERVERURL = os.getenv('Heroku_backend')
NEWSAPI_APIKEY = os.getenv('NEWSAPI_APIKEY')

def get_lastNews_datetime(news_website):
    last_news = get_newslist(news_website, 1)
    return last_news['data']['news'][0]['news_datetime']

def get_newslist(news_website, limit):
    my_params = json.dumps({'news_website': news_website, 'limit': limit})
    res = requests.get(backend_SERVERURL+'/newslist', params=my_params)
    results = res.json()
    return results

def post_newslist(newslist):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'news': newslist})
    res = requests.post(backend_SERVERURL+'/newslist', headers=headers, data=payload)
    results = res.json()
    return results

def get_newsapi(last_date):
    res = requests.get('https://newsapi.org/v2/everything?sources=bbc-news&q=bitcoin&from='+str(last_date)+'&sortBy=publishedAt&apiKey='+str(NEWSAPI_APIKEY))
    results = res.json()
    return results

def get_bbcPage():
    res = requests.get('https://www.bbc.com/news/topics/c734j90em14t/bitcoin')
    return res

def get_bbcNews_json(bbc_url):
    res = requests.get(bbc_url)
    return res.json()