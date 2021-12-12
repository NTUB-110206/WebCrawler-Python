from bs4 import BeautifulSoup
from app import WEB_API
from app import utils

def get_newsBitcoin_totalPage():
    newsBitcoinPage = WEB_API.get_newsBitcoin()
    soup = BeautifulSoup(newsBitcoinPage.text,"html.parser")
    total_page_number = (soup.select("div.page-nav.td-pb-padding-side a.last")[0].text).replace(',', '')
    print('總頁數: '+total_page_number+' 頁\n')
    return int(total_page_number)

def get_newsBitcoin_news(last_date):
    total_page_number = get_newsBitcoin_totalPage()
    print(str(total_page_number)+"--call page num--")
    link_list = get_all_newsBitcoinlink(last_date, total_page_number)
    print(str(link_list)+"--call link_list--")
    return 123

def get_all_newsBitcoinlink(last_date, total_page_number):
    soupData=[]
    # for i in range(total_page_number+1):
    for i in range(5):
        print(str(i)+'--------------------------------')
        newsPage = WEB_API.get_newsBitcoinPages(str(i))
        soup = BeautifulSoup(newsPage.text,"html.parser")
        huge = soup.select("div.story.story--huge a")
        large = soup.select("div.story--large a")
        medium = soup.select("div.story--medium__info a")
        small = soup.select("div.story--small__text a")
        tiny = soup.select("div.story--tiny a")
        theme = soup.select("div.story--theme a")
        soupData.extend([huge, large, medium, small, tiny, theme])
        print(soupData)
        datetime = soup.select("div.story__footer span")
        for item in datetime:
            f_Datetime = utils.parseDatetime(item.text)
            print(f_Datetime)
            if last_date[:19] >= str(f_Datetime)[:19]:
                print(str(f_Datetime))
                break
        else:
            continue
        break
            
    links = list(set([item.get('href') for sublist in soupData for item in sublist]))
    print(len(links))

    return 123

def newsBitcoin_crawler():
    last_date = WEB_API.get_lastNews_datetime('NEWS.BITCOIN')
    print('last_date '+last_date)
    total_page_number = get_newsBitcoin_totalPage()
    print("total_page_number "+str(total_page_number))
    print(type(total_page_number))
    link_list = get_all_newsBitcoinlink(last_date, total_page_number)
    print("link_list "+str(link_list))
    
    return 'newsBitcoin'