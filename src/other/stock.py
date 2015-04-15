#!/usr/bin/python
#coding: utf8

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

if __name__ == '__main__':
	date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	data_path = 'data'
	if not os.path.isdir(data_path):
		os.mkdir(data_path)
	data_file = os.path.join(data_path, date + '.data')
	if os.path.isfile(data_file):
		sys.stderr.write("file '" + data_file + "' exists.\n")
		sys.exit(0)
	fin = open('stock.list', 'r')
	fout = open(data_file, 'w')
	for url in fin:
		url = url.strip()
		html = get_html(url)
		soup = BeautifulSoup(html)
		name = soup.find('div', class_='stockTitle').find('strong', class_='stockName').string.encode('utf-8')
		price = soup.find('div', class_='currentInfo').find('strong').string.encode('utf-8')
		#print '\t'.join([name, date, 'price', price, url])
		fout.write('\t'.join([name, date, 'price', price, url]) + '\n')
		top_table_tds = soup.find('table', class_='topTable').find_all('td')
		for td in top_table_tds:
			kv = ''.join(td.stripped_strings).encode('utf-8').split('：')
			key = kv[0]
			value = kv[1]
			#print '\t'.join([name, date, key, value, url])
			fout.write('\t'.join([name, date, key, value, url]) + '\n')
	fin.close()
	fout.close()
    
