#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import string
import re
from bs4 import BeautifulSoup
sys.path.append("..")
from base.Log import Log
from base.Data import Data
from base.Spider import Spider

all_funds_value_url = "http://www.howbuy.com/board/"
stock_funds_value_url = "http://www.howbuy.com/board/gupiao.htm"
hybrid_funds_value_url = "http://www.howbuy.com/board/hunhe.htm"
index_funds_value_url = "http://www.howbuy.com/board/zhishu.htm"

all_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/"
stock_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/gupiao.htm"
hybrid_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/hunhe.htm"
index_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/zhishu.htm"

fund_url_prefix = "http://www.howbuy.com/fund/"

def get_info_date():
	html = Spider.getHtml(all_funds_value_url)
	soup = BeautifulSoup(html)
	info = soup.find('div', class_='dataTables').find('div', class_='quotation')
	info_text = info.get_text().encode('utf-8')
	info_date = re.search(r'(\d+)-(\d+)-(\d+)', info_text).group(0)
	return info_date

def get_value_list(url):
	html = Spider.getHtml(url)
	soup = BeautifulSoup(html)
	head = ['FundCode','FundName','UnitValue','AccValue','PrevUnitValue','PrevAccValue','Increase','IncreaseRate']
	data = Data(head, [])
	table = soup.find('div', class_='dataTables').find('div', 'result_list')
	tr_list = table.find_all('tr')
	for tr in tr_list:
		item = []
		td_list = tr.find_all('td')
		if len(td_list) != 11:
			continue
		for td in td_list[2:10]:
			item.append(td.get_text().encode('utf-8'))
		data.addItem(item)
	return data

def get_ranking_list(url):
	html = Spider.getHtml(url)
	soup = BeautifulSoup(html)
	head = ['FundCode','FundName','Date','Value','WeeklyYield','MonthlyYield','QuarterlyYield','HalfYearYield','YearlyYield','ThisYearYield']
	data = Data(head, [])
	table = soup.find('div', class_='dataTables').find('div', 'result_list')
	tr_list = table.find_all('tr')
	for tr in tr_list:
		item = []
		td_list = tr.find_all('td')
		if len(td_list) != 14:
			continue
		for td in td_list[2:12]:
			item.append(td.get_text().encode('utf-8'))
		data.addItem(item)
	return data

if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		msg = "invalid arguments: "
		msg += " ".join(sys.argv)
		msg += "."
		Log.error(msg)
		sys.exit(1)

	output_path = sys.argv[1]
	if not os.path.isdir(output_path):
		os.mkdir(output_path)

	info_date = get_info_date().replace('-','')

	code_list = []

	# all funds value
	file_name = "all_funds_value." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	data = get_value_list(all_funds_value_url)
	data.dump(fout)
	fout.close

	# all funds ranking
	file_name = "all_funds_ranking." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	data = get_ranking_list(all_funds_ranking_url)
	data.dump(fout)
	fout.close

	# stock funds value
	file_name = "stock_funds_value." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	data = get_value_list(stock_funds_value_url)
	data.dump(fout)
	fout.close

	code_list += data.getReversedAttr('FundCode')

	# stock funds ranking
	file_name = "stock_funds_ranking." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	data = get_ranking_list(stock_funds_ranking_url)
	data.dump(fout)
	fout.close

	# hybrid funds value
	file_name = "hybrid_funds_value." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	data = get_value_list(hybrid_funds_value_url)
	data.dump(fout)
	fout.close

	code_list += data.getReversedAttr('FundCode')

	# hybrid funds ranking
	file_name = "hybrid_funds_ranking." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	data = get_ranking_list(hybrid_funds_ranking_url)
	data.dump(fout)
	fout.close

	# index funds value
	file_name = "index_funds_value." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	data = get_value_list(index_funds_value_url)
	data.dump(fout)
	fout.close

	code_list += data.getReversedAttr('FundCode')

	# index funds ranking
	file_name = "index_funds_ranking." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	data = get_ranking_list(index_funds_ranking_url)
	data.dump(fout)
	fout.close

	# latest stock position
	file_name = "latest_stock_position." + info_date + ".data"
	file_path = os.path.join(output_path, file_name)
	fout = open(file_path, 'w')
	code_list = set(code_list)
	data = Data()
	for code in code_list:
		data.cat(get_latest_stock_position(code))
	data.dump(fout)
	fout.close

