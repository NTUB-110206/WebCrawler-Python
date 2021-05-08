
import psycopg2
from config import config
def insert_news_list(news_list):
    """ insert multiple news into the news table  """
    # sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"
    sql = "INSERT INTO news(news_datetime, news_title, news_content, news_website, news_link) VALUES(%s,%s,%s,%s,%s)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,news_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
