#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import string
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.Log import Log
from base.Spider import Spider

all_funds_value_url = "http://www.howbuy.com/board/"
stock_funds_value_url = "http://www.howbuy.com/board/gupiao.htm"
hybrid_funds_value_url = "http://www.howbuy.com/board/hunhe.htm"
index_funds_value_url = "http://www.howbuy.com/board/zhishu.htm"

all_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/"
stock_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/gupiao.htm"
hybrid_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/hunhe.htm"
index_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/zhishu.htm"

fund_url_pattern= "http://www.howbuy.com/fund/CODE"
fund_top_stock_url_pattern = "http://jingzhi.funds.hexun.com/Detail/DataOutput/Top10HoldingStock.aspx?fundcode=CODE&date=DATE"

def get_info_date():

	try:
		html = Spider.getHtml(all_funds_value_url)
	except:
		Log.warning("failed to read '" + url + "'.")
		return pd.DataFrame()
	soup = BeautifulSoup(html)
	info = soup.find('div', class_='dataTables').find('div', class_='quotation')
	info_text = info.get_text().encode('utf-8')
	info_date = re.search(r'(\d+)-(\d+)-(\d+)', info_text).group(0)
	return info_date

def norm_value(x):

	if isinstance(x, str):
		if x == "--":
			return np.nan
		if x[-1] == '%':
			return float(x[:-1])/100
	return x

def get_fund_value(url):

	try:
		html = Spider.getHtml(url)
	except:
		Log.warning("failed to read '" + url + "'.")
		return pd.DataFrame()
	soup = BeautifulSoup(html)
	table = soup.find('div', class_='dataTables').find('div', 'result_list')
	n_col = 11
	data = [[] for i in range(n_col)]

	tr_list = table.find_all('tr')
	for tr in tr_list:
		item = []
		td_list = tr.find_all('td')
		if len(td_list) != n_col:
			continue

		for i in range(n_col):
			data[i].append(td_list[i].get_text().encode('utf-8'))

	data = pd.DataFrame({	'Code' : data[2],
							'Name' : data[3],
							'Unit Value' : data[4],
							'Acc Value' : data[5],
							'Prev Unit Value' : data[6],
							'Prev Acc Value' : data[7],
							'Increase' : data[8],
							'Daily Yield' : data[9]	})
	data = data.applymap(norm_value)
	return data

def get_fund_ranking(url):

	try:
		html = Spider.getHtml(url)
	except:
		Log.warning("failed to read '" + url + "'.")
		return pd.DataFrame()
	soup = BeautifulSoup(html)
	table = soup.find('div', class_='dataTables').find('div', 'result_list')
	n_col = 14
	data = [[] for i in range(n_col)]

	tr_list = table.find_all('tr')
	for tr in tr_list:
		item = []
		td_list = tr.find_all('td')
		if len(td_list) != n_col:
			continue

		for i in range(n_col):
			data[i].append(td_list[i].get_text().encode('utf-8'))

	df = pd.DataFrame({	'Code' : data[2],
							'Name' : data[3],
							'Weekly Yield' : data[6],
							'Monthly Yield' : data[7],
							'Quarterly Yield' : data[8],
							'Half-yearly Yield' : data[9],
							'Yearly Yield' : data[10]	})
	df = df.applymap(norm_value)
	return df

def get_fund_info():

	stock_funds_value = get_fund_value(stock_funds_value_url)
	hybrid_funds_value = get_fund_value(hybrid_funds_value_url)
	index_funds_value = get_fund_value(index_funds_value_url)
	
	stock_funds_ranking = get_fund_ranking(stock_funds_ranking_url)
	hybrid_funds_ranking = get_fund_ranking(hybrid_funds_ranking_url)
	index_funds_ranking = get_fund_ranking(index_funds_ranking_url)

	del stock_funds_ranking['Name']
	del hybrid_funds_ranking['Name']
	del index_funds_ranking['Name']
	stock_funds_data = pd.merge(stock_funds_value, stock_funds_ranking, on='Code')
	stock_funds_data['Type'] = 'stock'
	hybrid_funds_data = pd.merge(hybrid_funds_value, hybrid_funds_ranking, on='Code')
	hybrid_funds_data['Type'] = 'hybrid'
	index_funds_data = pd.merge(index_funds_value, index_funds_ranking, on='Code')
	index_funds_data['Type'] = 'index'
	data = pd.concat([stock_funds_data, hybrid_funds_data, index_funds_data])
	return data.reindex(columns=[	'Code', 'Name', 'Type', 'Unit Value', 'Acc Value', 'Prev Unit Value', 'Prev Acc Value', 'Increase', 
									'Daily Yield', 'Weekly Yield', 'Monthly Yield', 'Quarterly Yield', 'Half-yearly Yield', 'Yearly Yield'	])

def download_fund_info():

	d = get_fund_info()
	if d.empty:
		return False
	d.to_csv(FUND_INFO_DATA_PATH, index=False)
	return True

def get_fund_top_stock(code, date):

	url = fund_top_stock_url_pattern.replace("CODE", code).replace("DATE", date)
	try:
		html = Spider.getHtml(url)
	except:
		Log.warning("failed to read '" + url + "'.")
		return pd.DataFrame()
	soup = BeautifulSoup(html)
	table = soup.find('table')

	n_col = 5
	data = [[] for i in range(n_col)]

	tr_list = table.find_all('tr')
	if len(tr_list) <= 1:
		return pd.DataFrame()

	n_tr = 0
	for tr in tr_list[1:]:
		item = []
		td_list = tr.find_all('td')
		if len(td_list) != n_col:
			continue

		n_tr += 1
		for i in range(n_col):
			data[i].append(td_list[i].get_text().encode('utf-8'))
	if n_tr == 0:
		return pd.DataFrame()

	df = pd.DataFrame({	'Code' : code,
							'Stock Name' : data[0],
							'Stock Price' : data[1],
							'Stock Increase' : data[2],
							'Stock Volume' : data[3],
							'Stock Position' : data[4]	})
	df = df.applymap(norm_value)
	return df.reindex(columns=['Code', 'Stock Name', 'Stock Price', 'Stock Increase', 'Stock Volume', 'Stock Position'])

def download_fund_top_stock(code_list, date, path):

	file_path = os.path.join(path, date+".csv")
	data = pd.DataFrame()
	for code in code_list:
		d = get_fund_top_stock(code, date)
		data = pd.concat([data, d])
	if data.empty:
		return False
	if os.path.isfile(file_path):
		os.remove(file_path)
	data.to_csv(file_path, index=False)
	return True

def download_all_fund_top_stock(path):

	fund_info_df = get_fund_info()
	code_list = fund_info_df['Code']
	today = time.strftime('%Y-%m-%d')
	current_year = int(time.strftime('%Y'))
	for year in range(2010, current_year+1):
		for month_date in ['03-15', '06-15', '09-15', '12-15']:
			date = str(year) + '-' + month_date
			if date < today:
				download_fund_top_stock(code_list, date, path)
	return True

def download_new_fund_top_stock():

	fund_info_df = get_fund_info()
	code_list = fund_info_df['Code']
	today = time.strftime('%Y-%m-%d')
	current_year = int(time.strftime('%Y'))
	prev_year = current_year - 1
	q0 = str(prev_year) + '-12-15'
	q1 = str(current_year) + '-03-15'
	q2 = str(current_year) + '-06-15'
	q3 = str(current_year) + '-09-15'
	q4 = str(current_year) + '-12-15'
	for date in [q4, q3, q2, q1, q0]:
		if today > date:
			break
	if not os.path.isdir(FUND_TOP_STOCK_PATH):
		os.mkdir(FUND_TOP_STOCK_PATH)
	download_fund_top_stock(code_list, date, FUND_TOP_STOCK_PATH)
	return True

if __name__ == '__main__':

	# download fund info
	download_fund_info()

	# download top stock position of all funds
	download_new_fund_top_stock()

