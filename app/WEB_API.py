import os
import requests  
backend_SERVERURL = os.getenv('Heroku_backend')
NEWSAPI_APIKEY = os.getenv('NEWSAPI_APIKEY')

def get_newslist(news_website, limit):
    my_params = {'news_website': news_website, 'limit': limit}
    res = requests.get(backend_SERVERURL+'/newslist', params=my_params)
    results = res.json()
    return results

def get_newsapi(last_date):
    res = requests.get('https://newsapi.org/v2/everything?sources=bbc-news&q=bitcoin&from='+str(last_date)+'&sortBy=publishedAt&apiKey='+str(NEWSAPI_APIKEY))
    results = res.json()
    return results
