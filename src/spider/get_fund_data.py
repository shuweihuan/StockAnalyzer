#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import string
import re
from bs4 import BeautifulSoup
sys.path.append("..")
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

latest_stock_position_url_prefix = "http://jingzhi.funds.hexun.com/Detail/DataOutput/Top10HoldingStock.aspx?fundcode="
fund_stock_url_prefix = "http://jingzhi.funds.hexun.com/database/cgmx.aspx?fundcode="

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

if __name__ == '__main__':
	
#	date = time.strftime('%Y-%m-%d',time.localtime(time.time()))

	fout = open('test.data', 'w')

	info_date = get_info_date()
	fout.write(info_date + '\n')

	fout.write('\n')

	data = get_value_list(all_funds_value_url)
	data.dump(fout)

	fout.write('\n')

	data = get_ranking_list(all_funds_ranking_url)
	data.dump(fout)

	fout.write('\n')

	data = get_latest_stock_position("070021")
	data.dump(fout)

	fout.write('\n')

	fout.close()
