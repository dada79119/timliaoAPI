import requests
import ssl
from bs4 import BeautifulSoup
import time
import os
import urllib.request
import json

# ssl._create_default_https_context = ssl._create_unverified_context

# asign URLs
TIMLIAO_URL = 'http://www.timliao.com/bbs/forumdisplay.php'

# srapy Index
def srapy(url):
    payload = {'fid': 18, 'page': '1'}
    re = requests.get(url = url, params=payload)
    returnText = BeautifulSoup(re.text, 'html.parser')

    return returnText

# def srapy(url):
#     for page_num in range (1, 11):
#         payload = {'fid': 18, 'page': page_num}
#         print(payload)
#     return payload    
#     re = requests.get(url = url, params=payload)
#     returnText = BeautifulSoup(re.text, 'html.parser')

#     return returnText


def get_link(dom):
    articleLink=[]
    for article in dom.findAll("h2",{'class','subject'}):
        if article.a.get('href') != None and len(article.a.get('href')) == 24:
            link = 'http://www.timliao.com/bbs/'+article.a.get('href')
            articleLink.append(link)

    return articleLink

def download_pic(link):
    time.sleep(0.5)
    re = requests.get(url = link)
    soup = BeautifulSoup(re.text, 'html.parser')
    getImageHead = soup.find("h1",{'class','head'})
    headTitle = getImageHead.text.strip()[0:256].encode('ISO-8859-1').decode('big5')
    getImageLink = soup.findAll("img",{'class','imglimit'})
    for Imgsrc in getImageLink:
        if u'scontent-tpe1-1' in Imgsrc['src'] or u'imgur' in Imgsrc['src']:
            try:
                if not os.path.isdir(headTitle):
                    os.mkdir(headTitle)
                fname = Imgsrc['src'].split('/')[-1]
                urllib.request.urlretrieve(Imgsrc['src'], os.path.join(headTitle, fname))
            except Exception as e:
                print(e)

def print_pic_json(link):
    time.sleep(0.5)
    re = requests.get(url = link)
    soup = BeautifulSoup(re.text, 'html.parser')
    articles = []
    getImageHead = soup.find("h1",{'class','head'})    
    headTitle = getImageHead.text.strip()[0:256].encode('ISO-8859-1').decode('big5')
    print(headTitle)
    getImageLink = soup.findAll("img",{'class','imglimit'})
    for Imgsrc in getImageLink:
        # print(Imgsrc)
        if u'scontent-tpe1-1' in Imgsrc['src'] or u'imgur' in Imgsrc['src']:
            try:
                    
                    fname = Imgsrc['src']+',' 


                    json_link = {
                        'title':headTitle,
                        'pic':fname
                    };
                    # print(json_link);
                    with open('data.json', 'w', encoding='utf-8') as f:
                        json.dump(json_link, f, indent=2, sort_keys=True, ensure_ascii=False)
    


            except Exception as e:
                print(e)

if __name__ == '__main__':
    # articles = []
    content = srapy(TIMLIAO_URL)
    IndexArray = get_link(content)
    # print(IndexArray)

    for link in IndexArray:
       
        # articles = 
        # srapy(url)
        # download_pic(link) #下載圖片
        print_pic_json(link) #圖片網址




