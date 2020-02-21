import requests
import pandas as pd
import json
import sqlite3
from bs4 import BeautifulSoup



headers = {"User-Agent": "ittensive-python-scraper/1.0 (+https://www.ittensive.com/)"}
link = 'https://video.ittensive.com/data/018-python-advanced/beru.ru/'
r = requests.get(link, headers = headers)
html = BeautifulSoup(r.content, features="lxml")

def find_links (links, keyword):
    links_filtered = {}
    for link in links:
        
        if link.has_attr("href") and link["href"].find(keyword) == 0:
            links_filtered[link["href"]] = 1
    return list(links_filtered.keys())

urls = []
urls.extend(find_links(html.find_all("a"), "kholodilnik"))

conn = sqlite3.connect("C:\\SQlite\\data.db3")
db = conn.cursor()
db.execute("DROP TABLE beru_goods")
conn.commit()
db.execute("""CREATE TABLE beru_goods
                  (id INTEGER PRIMARY KEY AUTOINCREMENT not null,
                   url text,
                   title text default '',
                   price FLOAT default 0,
                   width FLOAT default 0,
                   height FLOAT default 0,
                   length FLOAT default 0,
                   comm_volume FLOAT default 0,
                  cold_store FLOAT default 0
                   )
""")
conn.commit()

for url in urls:
    u = requests.get(link + url)
    detail = BeautifulSoup(u.content, features="lxml")
    price = detail.find("div", {"data-auto" : "price"}).get_text().split()
    price = float(price[0]+price[1])
    title = detail.find("div", {"data-zone-name" : "summary"}).find("div", {"class" : "section"}).find("h1").get_text()
    url= link + url
    li = detail.find("div", {"data-zone-name" : "specs"}).find("ul").find_all("li")
    h = 0.0
    w = 0.0
    length = 0.0
    all_am = 0.0
    h_am = 0.0
    for l in li:
      #print(l.get_text())
      if l.get_text().find("ШхВхГ") != -1:
        w = float(l.get_text().replace("ШхВхГ: ", "").replace(" см", "").split("х")[0])
        h = float(l.get_text().replace("ШхВхГ: ", "").replace(" см", "").split("х")[1])
        length = float(l.get_text().replace("ШхВхГ: ", "").replace(" см", "").split("х")[2])
      elif l.get_text().find("общий объем") != -1:
        all_am = float(l.get_text().replace("общий объем ", "").replace(" л", ""))
      elif l.get_text().find("объем холодильной камеры") != -1:
        h_am = float(l.get_text().replace("объем холодильной камеры ", "").replace(" л", ""))
      else:
        continue
    db.execute("INSERT INTO beru_goods (url, title, price, width, height, length, comm_volume, cold_store) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (url, title, price, h, w, length, all_am, h_am))
    conn.commit()
    #print(url, title, price, w,h,length,all_am,h_am)


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

data = pd.read_sql_query("SELECT * FROM beru_goods", conn)
print (data)

db.close()

input()
