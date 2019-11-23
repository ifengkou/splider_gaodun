#!/usr/bin/python3
#coding=utf-8
from logger import Logger
import json
import requests
import urllib
import string
from urllib.parse import quote
from bs4 import BeautifulSoup
import csv

def handle_price(price):
    price = str.replace(price,'¥','')
    price = str.replace(price,'"','')
    price = str.replace(price,',','')
    return float(price.strip())

def handle_buys(buys):
    buys = str.replace(buys,'已有','')
    buys = str.replace(buys,'人买过','')
    return int(buys.strip())

def writeToCSV(courses):
    with open('result2.csv', 'a',newline='',encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        rows = []
        for c in courses:
            row = [c['cata'],c['title'],c['price'],c['old_price'],c['buy_numb']]
            rows.append(row)
        writer.writerows(rows)

class GaodunService:
    def __init__(self):
        self.logging = Logger().get_log()
        self.query_url = "https://v.gaodun.com/course"
        self.catalogs = {'z1':'国内财会证书','z2':'国际财会证书','z12':'金融证书','z11':'职业发展','z5':'投资理财','z16':'考研','z13':'海外留学','z14':'青少年商业课程'}
        self.pagesize = {'z1':3,'z2':2,'z12':13,'z11':6,'z5':1,'z16':1,'z13':1,'z14':1}
        HEADER_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'
        self.HEADER ={
            'User-Agent': HEADER_USER_AGENT,
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,hu;q=0.6',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
    def writeToFile(self,courses):
        with open('result.csv', 'a') as f:
            for c in courses:
                course_str = ','.join([c['cata'],c['title'],c['price'],c['old_price'],c['buy_numb']])
                f.write('\n'+course_str)

    def parseSinglePage(self,cata,page):
        url = self.query_url+'/' + cata + 'p'+ page
        catastr = self.catalogs.get(cata)
        self.logging.info('开始搜索网址:%s' % (url))
        response = requests.get(url, {} , headers=self.HEADER, timeout=20,verify=False)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content,'html5lib')
        dom_divs = soup.find_all('div',class_='u-c-courseBlo')
        course_list = []
        if dom_divs:
            size = len(dom_divs)
            for dom in dom_divs:
                course = {}
                course['title'] = str.replace(dom.select('.d-tit > h2')[0].get_text(),',','') 
                
                price = dom.select('.d-price > .d-price-now')[0].get_text()
                course['price'] = handle_price(price)

                old_price = course['price']
                old_price_dom = dom.select('.d-price > .d-price-cost')
                if(old_price_dom):
                    old_price = old_price_dom[0].get_text()
                    old_price = handle_price(old_price)
                course['old_price'] = old_price

                buy_numb = dom.select('.d-price > .d-tip')[0].get_text()
                course['buy_numb'] = handle_buys(buy_numb)
                course['cata']= catastr
                course_list.append(course)

        if len(course_list) > 0:
            writeToCSV(course_list)    

    def start(self):
        for c in self.catalogs.keys():
            pageNum = self.pagesize.get(c)
            for i in range(1,pageNum+1):
                self.parseSinglePage(c,str(i))

gaodun = GaodunService()
#gaodun.parseSinglePage('z1',str(1))
gaodun.start()