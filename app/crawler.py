from bs4 import BeautifulSoup
import re
from app.WEB_API import *

def get_bbc_newsPage():
    bbcPage = get_bbcPage()
    soup = BeautifulSoup(bbcPage.text, "html.parser")  # 將網頁資料以html.parser
    total_page_number = soup.select("div.lx-pagination__details.gs-u-ph.qa-pagination-details span.lx-pagination__page-number.qa-pagination-total-page-number")[0].text
    print('總頁數: '+total_page_number+' 頁\n')

    return int(total_page_number)

def get_bbc_newsPage_url(total_page_number):
    u1 = 'https://push.api.bbci.co.uk/batch?t=%2Fdata%2Fbbc-morph-%7Blx-commentary-data-paged%2Fabout%2Fe0031680-9c66-4936-92b5-2ba0f88bc13c%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F'
    u2 = '%2Fversion%2F1.5.4%2Clx-commentary-data-paged%2Fabout%2Fe0031680-9c66-4936-92b5-2ba0f88bc13c%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F'
    u3 = '%2Fversion%2F1.5.4%7D?timeout=5'

    for i in range(1, total_page_number):
        u1 = u1+str(i)+u2
    uuu = u1+str(total_page_number)+u3
    return uuu

def get_bbc_news(last_date):
    print(last_date)
    total_page_number = get_bbc_newsPage()
    bbc_url = get_bbc_newsPage_url(total_page_number)
    result = get_bbcNews_json(bbc_url)
    news_list = []
    for newsPage in result['payload']:
        newsPages = newsPage['body']['results']
        for news in newsPages:
            new_news = {}
            new_news['news_title'] = news['title']
            new_news['news_datetime'] = str(news['dateAdded'])
            new_news['news_link'] = "https://www.bbc.com"+news['url'] if 'url' in news else "#"
            new_news['news_website'] = 'BBC'
            new_news['img_link'] = re.sub(r'http', 'https', news['image']['href']) if 'image' in news else "https://i.imgur.com/EJDC9vb.png"

            if 'summary' in news:
                new_news['news_content'] = news['summary']
            if 'synopses' in news:
                if news['synopses']['medium'] != None:
                    new_news['news_content'] = news['synopses']['medium']
                elif news['synopses']['short'] != None:
                    new_news['news_content'] = news['synopses']['short']
                elif news['synopses']['long'] != None:
                    new_news['news_content'] = news['synopses']['long']
            # CSP、STY 正常貼文 敘述在['summary']
            # MAP 影片
            # CLIP 敘述在['synopses']['medium'] 有short medium long
            # POST 類似FB twitter貼文只有title沒有網址、內容敘述
            news_list.append(new_news)
            if last_date[:19] >= str(news['dateAdded'])[:19]:
                news_list.pop()
                print(str(news['dateAdded']))
                break
        else:
            continue
        break

    # 多存一個所以pop出來
    return news_list

