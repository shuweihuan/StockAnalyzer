#!/usr/bin/python
#coding: utf-8

import os
import sys
import time
import string
import re
from bs4 import BeautifulSoup
sys.path.append("..")
from base.Log import Log
from base.File import File
from base.Data import Data
from base.Spider import Spider

latest_stock_position_url_prefix = "http://jingzhi.funds.hexun.com/Detail/DataOutput/Top10HoldingStock.aspx?fundcode="
stock_position_url_pattern = "http://jingzhi.funds.hexun.com/Detail/DataOutput/Top10HoldingStock.aspx?fundcode=xxxxxx&date=yyyy-mm-dd"

def get_latest_stock_position(code):
	url = latest_stock_position_url_prefix + code
	html = Spider.getHtml(url)
	soup = BeautifulSoup(html)
	head = ['FundCode','StockName','StockPrice','Increase','StockVolume','StockPosition']
	data = Data(head, [])
	table = soup.find('table')
	tr_list = table.find_all('tr')
	for tr in tr_list[1:]:
		item = [code]
		td_list = tr.find_all('td')
		for td in td_list:
			item.append(td.get_text().encode('utf-8'))
		data.addItem(item)
	return data

def get_stock_position(code, date):
	url = stock_position_url_pattern
	url = url.replace("xxxxxx", code).replace("yyyy-mm-dd", date)
	html = Spider.getHtml(url)
	soup = BeautifulSoup(html)
	head = ['FundCode','StockName','StockPrice','Increase','StockVolume','StockPosition']
	data = Data(head, [])
	table = soup.find('table')
	tr_list = table.find_all('tr')
	for tr in tr_list[1:]:
		item = [code]
		td_list = tr.find_all('td')
		for td in td_list:
			item.append(td.get_text().encode('utf-8'))
		data.addItem(item)
	return data

def dump_stock_position_data(data_path, code_list, date):
	file_name = "stock_position." + date.replace('-','') + ".data"
	file_path = os.path.join(data_path, file_name)
	fout = open(file_path, 'w')
	code_list = set(code_list)
	data = Data([],[])
	for code in code_list:
		data.cat(get_stock_position(code, date))
	data.dump(fout)
	fout.close

if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		msg = "invalid arguments: "
		msg += " ".join(sys.argv)
		msg += "."
		Log.error(msg)
		sys.exit(1)

	raw_path = sys.argv[1]
	if not os.path.isdir(raw_path):
		os.mkdir(raw_path)

	data = Data()
	f = File.getLatestFile(raw_path, "stock_funds_value")
	data.load(f)
	code_list = data.getReversedAttr("FundCode")

	#dump_stock_position_data(raw_path, code_list, "2015-03-15")
	#dump_stock_position_data(raw_path, code_list, "2014-12-15")
	#dump_stock_position_data(raw_path, code_list, "2014-09-15")
	#dump_stock_position_data(raw_path, code_list, "2014-06-15")
	#dump_stock_position_data(raw_path, code_list, "2014-03-15")
	#dump_stock_position_data(raw_path, code_list, "2013-12-15")
	#dump_stock_position_data(raw_path, code_list, "2013-09-15")
	#dump_stock_position_data(raw_path, code_list, "2013-06-15")
	#dump_stock_position_data(raw_path, code_list, "2013-03-15")
	#dump_stock_position_data(raw_path, code_list, "2012-12-15")
	#dump_stock_position_data(raw_path, code_list, "2012-09-15")
	#dump_stock_position_data(raw_path, code_list, "2012-06-15")
	#dump_stock_position_data(raw_path, code_list, "2012-03-15")
	dump_stock_position_data(raw_path, code_list, "2011-12-15")
	dump_stock_position_data(raw_path, code_list, "2011-09-15")
	dump_stock_position_data(raw_path, code_list, "2011-06-15")
	dump_stock_position_data(raw_path, code_list, "2011-03-15")
	dump_stock_position_data(raw_path, code_list, "2010-12-15")
	dump_stock_position_data(raw_path, code_list, "2010-09-15")
	dump_stock_position_data(raw_path, code_list, "2010-06-15")
	dump_stock_position_data(raw_path, code_list, "2010-03-15")

