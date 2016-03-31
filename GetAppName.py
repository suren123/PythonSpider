#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2
# import string
import re
import sys
import os
import threading
import threadpool
import time

#找所有银行
def findAllBanks():
    url = 'http://app.91.com/soft/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()

    # print(html)

    banks = re.findall(r'<h4>'
                       r'[^<>]*'
                       r'<a href="(.*?\.html).*?">(.*?)</a>'
                       r'</h4>', html, re.S)

    # banks = re.findall('<img src="(.*?)" width="150" height="46" alt="(.*?)">', html, re.S)
    #
    # print(banks)

    for bank in banks:
        print(bank[0])
        print(bank[1])
        # print(bank.strip())

findAllBanks()