#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import string
import urllib2
import re
from bs4 import BeautifulSoup

latest_stock_position_url_prefix = "http://jingzhi.funds.hexun.com/Detail/DataOutput/Top10HoldingStock.aspx?fundcode="
fund_stock_url_prefix = "http://jingzhi.funds.hexun.com/database/cgmx.aspx?fundcode="

def get_html(url):
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0')
	opener = urllib2.build_opener()
	html = opener.open(request).read()
	return html

def get_latest_stock_position(code):
	url = latest_stock_position_url_prefix + code
	html = get_html(url)
	soup = BeautifulSoup(html)
	data_body = soup.find('table')
	data = []
	tr_list = data_body.find_all('tr')
	for tr in tr_list[1:]:
		td_list = tr.find_all('td')
		s = ""
		s += td_list[0].get_text().encode('utf-8')
		s += "\t"
		s += td_list[3].get_text().encode('utf-8')
		s += "\t"
		s += td_list[4].get_text().encode('utf-8')
		data.append(s)
	return data

def output_latest_stock_position_head(fout):
	fout.write("#FundCode\tStockName\tStockVolume\tStockPosition\n")
	
def output_latest_stock_position_data(fout, code, data):
	for i in data:
		fout.write(code + "\t" + i + "\n")

if __name__ == '__main__':
	
	# environment
	date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	data_path = "data"
	if not os.path.isdir(data_path):
		os.mkdir(data_path)

#	data = get_latest_stock_position("070001")
#	output_latest_stock_position_head(sys.stdout)
#	output_latest_stock_position_data(sys.stdout, data)

	stock_funds_stock_position_file = os.path.join(data_path, "stock_funds_stock_position" + ".data")
	if os.path.isfile(stock_funds_stock_position_file):
		sys.stderr.write("warning: file '" + stock_funds_stock_position_file + "' exists.\n")
	fout = open(stock_funds_stock_position_file, 'w')

	input_file = os.path.join(data_path, "stock_funds_ranking.20150414.data")
	fin = open(input_file, 'r')
	output_latest_stock_position_head(fout)
	for line in fin:
		line = line.strip()
		f = line.split('\t')
		code = f[1]
		data = get_latest_stock_position(code)
		output_latest_stock_position_data(fout, code, data)
	fin.close()
	fout.close()
	
