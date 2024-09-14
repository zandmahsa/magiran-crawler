import requests
from bs4 import BeautifulSoup
import re
import json
from time import sleep
from urllib.parse import unquote

# Variables
all_links=[]
dley= 60
dley2 = 3

# Load links and JSON data
with open('./links.txt') as f:
    for i in f:
        all_links.append(i.strip('\n'))
	    
with open('json.json','r',encoding='utf-8-sig') as f:
	js = json.loads(f.readline())

# HTTP headers
headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Language': 'en-US,en;q=0.5',
      'Content-Type': 'application/json; charset=utf-8',
      'X-Requested-With': 'XMLHttpRequest',
      'Origin': 'https://www.magiran.com',
      'Connection': 'keep-alive',
      'TE': 'Trailers',
     }

paper = 'https://www.magiran.com/paper/'
s = requests.Session()
s.headers.update(headers)
data = {"a":"", "coId":"", "p":2, "name":""}


# Main scraping loop
for i in all_links:
    try:
        sleep(dley2)
        res=s.get(i)
        links = re.findall('fa_(\d{1,10})',res.text)
        is_load = re.findall('\"moreInfoButton',res.text)
    except Exception as E:
        print(E)
    if is_load == []:
        is_load = False
    else:
        is_load = True ###
    name = unquote(i).split('/')[-1]

    # Pagination if more info is available
    if is_load:
        for j in range (2,100):
            try:
                data['a']=name
                data['p']= j
                sleep(dley2)
                res1=s.post('https://www.magiran.com/author/pagedindex',json=data)
                links_n = re.findall('fa_(\d{1,10})',res1.text)
                if links_n == []:
                    break
                links+=links_n
            except Exception as E:
                print(E)
    # Data structure for author and articles
    dict0={'نام':name,'مقالات':[]}

    # Scrape each article
    for ii in links:
        try:
            sleep(dley2)
            res = s.get(paper+str(ii))
            so =BeautifulSoup(res.text,'html.parser')
            ti=so.select('.py-2')[0].text
		
	    # Initialize article details
            key,athor,entesharat,lang,typem,pages='','','','','',''
            athor=so.select('.paper-info > div:nth-child(1) > div:nth-child(2)')[0].text.replace('\n','')

		
            for i in range(2,11):
                try:
                    ttt=so.select('div.row:nth-child('+str(i)+') > div:nth-child(1)')[0].text
                    
                    if ttt == 'کلیدواژگان:' or ttt == 'کلیدواژه:':
                        key = so.select('div.row:nth-child('+str(i)+') > div:nth-child(2)')[0].text.replace('\n','')
                    elif ttt== 'زبان:':
                        lang = so.select('div.row:nth-child('+str(i)+') > div:nth-child(2)')[0].text.replace('\n','')
                    elif ttt=='انتشار در:':
                        entesharat =so.select('div.row:nth-child('+str(i)+') > div:nth-child(2)')[0].text.replace('\n','')
                    elif ttt=='صفحات:' or ttt=='صفحه:':
                        pages=so.select('div.row:nth-child('+str(i)+') > div:nth-child(2)')[0].text.replace('\n','')
                    elif ttt=='نوع مقاله:':
                        typem=so.select('div.row:nth-child('+str(i)+') > div:nth-child(2)')[0].text.replace('\n','')
                except:
                    pass
            short_link=paper+str(ii)
            print('!!!!!!!!!!!!!!!!!!!!')
            print(ti)
            print(key)
            print(athor)
            print(entesharat)
            print(short_link)
            print(lang)
            print(typem)
            dict0['مقالات'].append({'عنوان':ti,'نويسنده':athor,'صفحات':pages,'کليد واژه':key,'انتشارات':entesharat,'لينک کوتاه':short_link,'زبان':lang,'نوع مقاله':typem})
            if dict0 not in js['res']:
                js['res'].append(dict0)
        except Exception as E:
            print(E)
    # Save the updated data
    with open('json.json','w',encoding='utf8') as f:
        f.write(json.dumps(js,ensure_ascii=False))
    sleep(dley)
