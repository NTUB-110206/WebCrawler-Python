
import psycopg2
from config import config
def select_news_lastdate(website):
    """ query data from the vendors table """
    conn = None
    result = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT news_datetime FROM bcd_news WHERE news_website=%s ORDER BY news_datetime desc LIMIT 1", (website,))
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            result=row
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result[0]