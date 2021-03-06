import requests
import ssl
from bs4 import BeautifulSoup
import time
import os
import urllib.request
import json
from flask import Flask, render_template, request, redirect, session, jsonify

# ssl._create_default_https_context = ssl._create_unverified_context
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
            link = article.a.get('href')[-5:]
            articleLink.append(link)
    return articleLink


def scrapyImg(link):
    time.sleep(0.5)
    re = requests.get(url = link)
    soup = BeautifulSoup(re.text, 'html.parser')
    getImageHead = soup.find("h1",{'class','head'})
    # print(getImageHead)
    headTitle = getImageHead.text.strip()[0:256].encode('ISO-8859-1','ignore').decode('big5')
    # print(headTitle)
    getImageLink = soup.findAll("img",{'class','imglimit'})
    src = ''
    for Imgsrc in getImageLink:
        if u'scontent-tpe1-1' in Imgsrc['src'] or u'imgur' in Imgsrc['src'] or u'instagram' in Imgsrc['src']:
            src+= Imgsrc['src']+','
    jsonStr = {
        'Title':headTitle,
        'Imgsrc':src[:-1]
    }
    return jsonStr
    



# flask route set
app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'GET':
        if request.args.get('get_tid') == 'true':
            content = srapy(TIMLIAO_URL)
            IndexArray = get_link(content)
    return jsonify(IndexArray)
    '''
    PicArray = []
    jsonArray = []
    content = srapy(TIMLIAO_URL)
    IndexArray = get_link(content)
    count=0
    for link in IndexArray:
        return_json = scrapyImg(link)
        PicArray.append(return_json)
        while len(PicArray)>count:
            # jsonArray.append(PicArray[count])
            # return jsonify(jsonArray)
            count = count+1
    return jsonify(PicArray)
    '''
app.run(port=5000, debug=True)




