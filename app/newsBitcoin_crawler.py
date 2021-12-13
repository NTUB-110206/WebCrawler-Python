from app import WEB_API
from app import utils
from bs4 import BeautifulSoup
from flask import jsonify

def get_newsBitcoin_totalPage():
    newsBitcoinPage = WEB_API.get_newsBitcoin()
    soup = BeautifulSoup(newsBitcoinPage.text,"html.parser")
    total_page_number = (soup.select("div.page-nav.td-pb-padding-side a.last")[0].text).replace(',', '')
    return int(total_page_number)

def get_all_newsBitcoinlink(last_date, total_page_number):
    soupData=[]
    for i in range(total_page_number+1):
        newsPage = WEB_API.get_newsBitcoinPages(str(i))
        soup = BeautifulSoup(newsPage.text,"html.parser")
        huge = soup.select("div.story.story--huge a")
        large = soup.select("div.story--large a")
        medium = soup.select("div.story--medium__info a")
        small = soup.select("div.story--small__text a")
        tiny = soup.select("div.story--tiny a")
        theme = soup.select("div.story--theme a")
        soupData.extend([huge, large, medium, small, tiny, theme])
        datetime = soup.select("div.story__footer")
        for item in datetime:
            f_Datetime = utils.parseDatetime(item.text)
            
            if (last_date.replace("T", " "))[:19] >= str(f_Datetime)[:19]:
                print("BREAK", str(f_Datetime))
                break
        else:
            continue
        break
            
    link_list = list(set([item.get('href') for sublist in soupData for item in sublist]))

    return link_list

def single_news_crawler(link_list):
    news_list=[]
    for link in link_list:
        news = WEB_API.get_newsBitcoin_singleNews(link)
        single_news_soup = BeautifulSoup(news.text,"html.parser")
        new_news = {}
        new_news['news_link'] = link
        new_news['news_title'] = (single_news_soup.select("article.article__body h1"))[0].text.replace('\n', '').replace('  ', '').replace('\t', '')
        new_news['news_content'] = (single_news_soup.select("article.article__body p"))[0].text
        new_news['news_datetime'] = str(utils.parseDatetime(single_news_soup.select("aside.article__info div.article__info__right time.article__info__date")[0].text.replace('\n', '').replace('  ', '').replace('\t', '')))
        new_news['news_website'] = 'NEWS.BITCOIN'
        new_news['img_link'] = (single_news_soup.select("article.article__body div.featured_image_container img"))[0]['src']
        news_list.append(new_news)
    return news_list

def newsBitcoin_crawler():
    last_date = WEB_API.get_lastNews_datetime('NEWS.BITCOIN')
    print('last_date '+last_date)
    total_page_number = get_newsBitcoin_totalPage()
    print('總頁數: '+str(total_page_number)+' 頁')
    link_list = get_all_newsBitcoinlink(last_date, total_page_number)
    print(link_list)
    print('link_list total', len(link_list))
    newslist = single_news_crawler(link_list)
    print(newslist)
    # len(news)>0就送給後端, 否則回覆 "no new news"
    result = WEB_API.post_newslist(newslist) if len(newslist) > 0 else jsonify({"result": "no new news"})
    print(result)
    return result