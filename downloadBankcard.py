#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2
# import string
import re
import os
import threading
import threadpool
import time

#找所有银行
def findAllBanks():
    url = 'http://kaku.51credit.com/shtml/banks.shtml'
    response = urllib2.urlopen(url)
    html = response.read()

    banks = re.findall('<li><a title=".*?" href="(.*?)" target="_blank">', html, re.S)
    for bank in banks:
        if bank.count('citibank') == 0:
            print(bank)
            bankIndex(bank)

# 银行首页
def bankIndex(bankurl):
    response = urllib2.urlopen(bankurl)
    html = response.read()
    findCardDetailPage(html)
    total = re.findall('<span>共(.*?)页 到第</span>', html, re.S)
    if len(total) > 0:
        print total[0]
        bankPage(bankurl, int(total[0]))


#银行每页
def bankPage(bankurl, end_page):
    for i in range(2, end_page+1):
        url = bankurl + 'index_' + str(i) + '.shtml'
        print url
        response = urllib2.urlopen(url)
        html = response.read()
        findCardDetailPage(html)


#寻找银行卡详情的url
def findCardDetailPage(html):
    cardDetailPages = re.findall('<h3><a href="(.*?)" target="_blank">.*?</a></h3>', html, re.S)
    for cardDetailPage in cardDetailPages:
        print cardDetailPage
        #在新的线程下载银行卡信息
        task = threading.Thread(target=downloadBankCard,args=(cardDetailPage,))
        task.start()

        #顺序下载银行卡信息
        #downloadBankCard(cardDetailPage)

        #在线程池中下载银行卡信息
        #requests = threadpool.makeRequests(downloadBankCard, (cardDetailPage,))
        #[pool.putRequest(req) for req in requests]


#从银行卡详情页面抓取数据
def downloadBankCard(url):
    picture_url = url.replace('index', 'picture')
    #替换url中的空格
    picture_url = urllib.quote(picture_url, safe="%/:=&?~#+!$,;'@()*[]")
    response = urllib2.urlopen(picture_url)
    html = response.read()

    type = re.findall('<h2 class="most_name"><a>(.*?)</a></h2>', html, re.S)
    print type[0]

    x = 0
    myItems = re.findall('<td><img width="186" height="117" src="(.*?)"/>', html, re.S)
    for item in myItems:
        #要先创建文件夹才能开始复制
        filename = 'img/' + type[0] + '_' + str(x) + '.jpg'
        urllib.urlretrieve(item, filename)
        print item
        x+=1

#创建目录
def mkdir(path):
    path = path.strip()
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


#入口
start_time = time.time()

#定义线程池
pool = threadpool.ThreadPool(300)
findAllBanks()
#全部结束
pool.wait()

print time.time()-start_time