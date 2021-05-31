# 爬取豆瓣电影TOP250的爬虫
import requests
from bs4 import BeautifulSoup
import time
import csv
import pymysql
# 从Chrome浏览器复制User-Agent，将其伪装成浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                 ' like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}

url = "https://movie.douban.com/top250"

ls = []


def get_info(url):
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text.encode('utf-8'), 'lxml')
    #print(soup.text)
    # 使用beautifulsoup解析代码,注意第一个参数的.text
    titles = soup.select('div.hd > a ')  # 有多项，之后再细分
    ranks = soup.select('div.pic > em ')
    rates = soup.select('div.star > span.rating_num')
    quotes = soup.select('p.quote > span.inq')
    staffs = soup.select('div.bd > p')
    #print(staffs)
    i=0
    for title, rank, rate, quote in zip(titles, ranks, rates,quotes):
        # # 获取影片的URL,从而得到name，但是这样容易被封IP
        # href = BeautifulSoup(str(title), 'lxml').find('a', attrs={'class': ''}, href=True).attrs['href']  # 找到a标签下，类名为，属性值
        # name=get_name(href)

        #name的替代方案，但是只有一个中文名
        name=title.select_one('span.title').get_text()
        # 某些电影没有quote，这里设法解决，但是悲惨的失败了
        # if rank.get_text() not in['175','183','192','213','225','226','239','250']:
        #     quote=staffs[i+1].get_text().strip()
        # else:
        #     continue

        # 去掉某些主演后面的无关信息
        sta=staffs[i].get_text().split('...')[0].strip().split('\xa0\xa0\xa0')
        if len(sta)>1:
            sta[1]=sta[1].split('\n')[0]
        data = {
            'rank':rank.get_text(),
            'name':name,
            'rate':rate.get_text(),
            'quote':quote.get_text(),
            'staff':sta
        }
        i+=2
        #print(data)
        ls.append(data)

def get_name(href):
    time.sleep(0.5)
    res = requests.get(href, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text.encode('utf-8'), 'lxml')
    name=soup.select_one('h1>span')
    if name != None:
        return name.get_text()
    else: return None

# 存储到数据库
def save_db(data):
    db = pymysql.connect(host="localhost", user="root", passwd="pass", db="douban",charset='utf8mb4')
    #获取游标
    cursor = db.cursor()
    for movie in data:
        sql="insert into top250 values({},'{}','{}',\"{}\",\"{}\")".format(
            movie['rank'], movie['name'],movie['rate'],movie['quote'],"/".join(movie['staff']))
        print(sql)
        cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    get_info(url)
    # 爬取2-10页的内容(1,10)这里是6页
    for i in range(1, 6):
        get_info('https://movie.douban.com/top250?start='+str(i*25))
        time.sleep(0.5)
    save_db(ls)


# #文件存储
# with open('douban_top250.csv', 'w', newline='',encoding='utf-8-sig')as f:  #在当前路径下，以写的方式打开一个文件，如不存在则创建
#     writer = csv.writer(f)
#     writer.writerow(['rank', 'name', 'rate', 'quote', 'staff'])
#     for movie in ls:
#         print(movie)
#         row = [movie['rank'], movie['name'],movie['rate'],movie['quote']]
#         staff = "/".join(movie['staff'])
#         row.append(staff)
#         writer.writerow(row)


