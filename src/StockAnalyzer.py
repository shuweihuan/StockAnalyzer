#!/usr/bin/python
#coding: utf-8

import os
import sys
import time
import string
import urllib2
from bs4 import BeautifulSoup

def get_html(url):
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0')
	opener = urllib2.build_opener()
	html = opener.open(request).read()
	return html

def get_stock_historical_data(code):
	url = "http://real-chart.finance.yahoo.com/table.csv?s=" + code
	return get_html(url)

if __name__ == '__main__':
	data = get_stock_historical_data("BIDU")
	print data
