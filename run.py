#!/usr/bin/python
#-*- coding:utf8 -*-

import sys
reload(sys)
sys.path.append('/Library/Python/2.7/site-packages')
sys.setdefaultencoding('utf-8')

import requests
import re
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
import json

class weixin_spider:
    def __init__(self, ):
        self.check = True

    def run(self, ename):
        self.search_url = "http://weixin.sogou.com/weixin?type=1&s_from=input&query=%s&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=6270" % ename
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0","Referer": self.search_url}
        maincontent = self.get_list(self.search_url)

    def get_list(self, search_url):
        html = requests.get(search_url, headers=self.headers, verify=False).content
        # print html
        selector = etree.HTML(html)
        # 提取文本
        content = selector.xpath('//div[@class="news-box"]/ul/li/div/div[@class="txt-box"]/p[@class="tit"]/a/@href')
        for list in content:
            print list
            maincontent = self.get_articals(list)
            # print maincontent

    def get_articals(self, wx_url):
        # browser = webdriver.Chrome('driver/chromedriver')
        # browser.get(wx_url)
        # page_source =  browser.page_source
        # print page_source
        html = requests.get(wx_url, headers=self.headers, verify=False).content
        # print html
        pattern = re.compile(r"(.*?)msgList = {(.*?)};(.*?)", re.DOTALL)
        articles = json.loads('{%s}' % pattern.match(html).group(2))
        for article in articles['list']:
            url = article['app_msg_ext_info']['content_url']
            url = url.replace('amp;','')
            html = requests.get('https://mp.weixin.qq.com%s' % url, headers=self.headers, verify=False).content
            print html
            break

        # selector = etree.HTML(html)


if __name__ == '__main__':
    print '''''
              *****************************************
              **    Welcome to Spider of 公众号爬虫       **
              **      Created on 2017-08--20          **
              **      @author: leon.si         **
              *****************************************
      '''

    # subscription = raw_input(u'输入要爬取的公众号')
    # if not subscription:
    #     subscription = 'Article'
    weixin_spider().run("VIP陪练家长联盟")

