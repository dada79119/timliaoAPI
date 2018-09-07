import requests
from bs4 import BeautifulSoup
import time
import os
import urllib.request

# asign URLs
TIMLIAO_URL = 'http://www.timliao.com/bbs/forumdisplay.php'

# srapy Index
def srapy(url):
    payload = {'fid': 18, 'page': '1'}
    re = requests.get(url = url, params=payload)
    returnText = BeautifulSoup(re.text, 'html.parser')
    return returnText

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

if __name__ == '__main__':
    content = srapy(TIMLIAO_URL)
    IndexArray = get_link(content)
    for link in IndexArray:
        download_pic(link)
