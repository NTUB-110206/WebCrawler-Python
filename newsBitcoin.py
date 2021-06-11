import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import re
import datetime
import pytz

from select_news_lastdate import select_news_lastdate
from insert_news_list import insert_news_list


def link_into_array(huge,large,medium,small,tiny):
  np_hyperlink = np.array([])
  for j in range(len(huge)): np_hyperlink=np.append(np_hyperlink, huge[j]["href"])
  for j in range(len(large)): np_hyperlink=np.append(np_hyperlink, large[j]["href"])
  for j in range(len(medium)): np_hyperlink=np.append(np_hyperlink, medium[j]["href"])
  for j in range(len(small)): np_hyperlink=np.append(np_hyperlink, small[j]["href"])
  for j in range(len(tiny)): np_hyperlink=np.append(np_hyperlink, tiny[j]["href"])
  np_hyperlink=np.unique(np_hyperlink)
  print(np_hyperlink)
  print(len(np_hyperlink))
  return np_hyperlink


if __name__ == '__main__':
  website="NEWS.BITCOIN"
  lastnews=str(select_news_lastdate(website))
  print(lastnews)
  # lastnews="2015-06-09T08:28:12.817Z"
  url = 'https://news.bitcoin.com/'
  r = requests.get(url)
  soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
  total_page_number = (soup.select("div.page-nav.td-pb-padding-side a.last")[0].text).replace(',', '') #
  print('總頁數: '+total_page_number+' 頁\n')
  hyperlink = np.array([]) #存連結用的
  for i in range(1, int(total_page_number)+1): #從page1爬到最後一頁
    news_list=[] #宣告tuple 將news存到tuple，再一起進資料庫
    print(type(news_list))
    print("i",i)
    uuu=url+'page/'+str(i)
    r = requests.get(uuu)
    soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
    huge = soup.select("div.story.story--huge a")
    large = soup.select("div.story--large a")
    medium = soup.select("div.story--medium__info a")
    small = soup.select("div.story--small__text a")
    tiny = soup.select("div.story--tiny a")
    hyperlink=np.append(hyperlink,link_into_array(huge,large,medium,small,tiny)) #第i頁的新聞連結全部存進np array
    count=0
    # for j in range(len(hyperlink)) :
    for j in (j for j in range(len(hyperlink)) if i % 3==0) : #i每跑3次進一次迴圈
      print("i",i,"j",j)
      # print(len(hyperlink))
      # print(hyperlink)
      date_add=''
      title=''
      content=''
      link=hyperlink[j]
      imglink=''
      # 點進連結 爬內容
      sub_r = requests.get(link)
      sub_soup = BeautifulSoup(sub_r.text,"html.parser") #將網頁資料以html.parser

      s_date_add = sub_soup.select("aside.article__info div.article__info__right time.article__info__date")[0].text.replace('\n', '').replace('  ', '').replace('\t', '')
      #取得此新聞的日期
      #並format格式
      if str(s_date_add).find("sec") != -1:
        date_add=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(seconds=int(re.sub('\D', '', s_date_add)))
      if str(s_date_add).find("min") != -1:
        date_add=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(minutes=int(re.sub('\D', '', s_date_add)))
      if str(s_date_add).find("hour") != -1:
        date_add=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(hours=int(re.sub('\D', '', s_date_add)))
      if str(s_date_add).find("day") != -1:
        date_add=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(days=int(re.sub('\D', '', s_date_add)))

      print("lastnews",type(lastnews),lastnews)
      print("dateadd",type(str(date_add)),str(date_add))
      if lastnews>=str(date_add):
        # 現有的新聞 比 這筆新聞還新
        # 代表資料庫已經 存在了
        # 不須再做後續
        count+=1 #計數舊新聞
        continue

      s_imglink=sub_soup.select("article.article__body div.featured_image_container img")
      imglink=s_imglink[0]["src"]
      s_content = sub_soup.select("article.article__body p")
      s_title=sub_soup.select("article.article__body h1")
      if len(s_title[0])>0 :
        title=s_title[0].text.replace('\n', '').replace('  ', '').replace('\t', '')
      if len(s_content[0])>0 :
        content=s_content[0].text
      print(i,j,date_add)
      print(i,j,title)
      # print(i,j,content)
      # print(i,j,link)
      # print(i,j,imglink)
      news_list.append((date_add,title,content,website,link,imglink)) #存進tuple
      # if lastnews>=str(date_add):
    #   if count==0:
    #     break
    # else:
    #   continue
    # break
    print("-----",i)
    if i % 3==0: #進資料庫
      news_list=sorted(news_list, reverse=True,key=lambda t:t[0])
      insert_news_list(news_list)
      print(news_list)
      news_list=[]
      hyperlink = np.array([])
      if count>10: break #舊新聞大於10則結束程式






