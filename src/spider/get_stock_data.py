#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import types
import string
import shutil
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import tushare as ts
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.Log import Log
from base.Time import Time
from base.Stock import Stock
from base.Spider import Spider

reload(sys)  
sys.setdefaultencoding('utf8')

stock_list_url = "http://quote.eastmoney.com/stocklist.html"
stock_history_url_pattern = "http://table.finance.yahoo.com/table.csv?s=CODE.MARKET"

def is_stock_code(code):
	if len(code) != 6:
		return False
	if code[:2] == "60" or code[:2] == "00" or code[:2] == "30":
		return True
	return False

def get_stock_market(code):
	if len(code) != 6:
		return "unknown"
	if code[:2] == "60":
		return "ss"
	if code[:2] == "00" or code[:2] == "30":
		return "sz"
	return "unknown"

def get_stock_list():
	try:
		html = Spider.getHtml(stock_list_url)
	except:
		Log.warning("failed to read '" + url + "'.")
		return pd.DataFrame()
	soup = BeautifulSoup(html, from_encoding='gbk')
	div = soup.find('div', id='quotesearch')
	li_list = div.find_all('li')
	code_list = []
	name_list = []
	url_list = []
	for li in li_list:
		text = li.a.get_text().encode('utf-8')
		text = text.replace('(', '\t').replace(')', '')
		f = text.split('\t')
		name = f[0]
		code = f[1]
		url = li.a.get('href')
		if is_stock_code(code):
			code_list.append(code)
			name_list.append(name)
			url_list.append(url)
	stock_list_df = pd.DataFrame({	'Code' : code_list,
									'Name' : name_list,
									'Url' : url_list	})
	return stock_list_df

def download_stock_list():
	d = get_stock_list()
	if d.empty:
		return False
	d.to_csv(STOCK_LIST_DATA_PATH, index=False)
	return True

def get_stock_data():
	d = ts.get_today_all()
	if type(d) == types.NoneType:
		return pd.DataFrame()
	return d

def download_stock_data():
	d = get_stock_data()
	if d.empty:
		return False
	d.to_csv(STOCK_DATA_PATH, index=False)
	return True

def get_index_data():
	d = ts.get_index()
	if type(d) == types.NoneType:
		return pd.DataFrame()
	return d

def download_index_data():
	d = get_index_data()
	if d.empty:
		return False
	d.to_csv(INDEX_DATA_PATH, index=False)
	return True

def get_stock_basics():
	d = ts.get_stock_basics()
	if type(d) == types.NoneType:
		return pd.DataFrame()
	return d

def download_stock_basics():
	d = get_stock_basics()
	if d.empty:
		return False
	d.to_csv(STOCK_BASICS_DATA_PATH)
	return True

def get_stock_report(year, quarter):
	d = ts.get_report_data(year, quarter)
	if type(d) == types.NoneType:
		return pd.DataFrame()
	d.loc[:,"code"] = d["code"].apply(Stock.norm_code)
	return d

def download_stock_report(year, quarter):
	d = get_stock_report(year, quarter)
	if d.empty:
		return False
	if not os.path.isdir(STOCK_REPORT_PATH):
		os.mkdir(STOCK_REPORT_PATH)
	f_name = str(year) + '-' + str(quarter) + ".csv"
	f = os.path.join(STOCK_REPORT_PATH, f_name)
	d.to_csv(f, index=False)
	return True

def download_all_stock_report():
	yq = Time.getLastQuarter()
	ly = yq[0]
	lq = yq[1]
	for y in range(2010, ly):
		for q in range(1, 5):
			download_stock_report(y, q)
	for q in range(1,lq+1):
		download_stock_report(ly, q)
	return True

def download_latest_stock_report():
	yq = Time.getLastQuarter()
	y = yq[0]
	q = yq[1]
	# 1st latest quarter
	download_stock_report(y, q)
	# 2nd latest quarter
	if q == 1:
		download_stock_report(y-1, 4)
	else:
		download_stock_report(y, q-1)
	return True

def get_stock_profit(year, quarter):
	d = ts.get_profit_data(year, quarter)
	if type(d) == types.NoneType:
		return pd.DataFrame()
	d.loc[:,"code"] = d["code"].apply(Stock.norm_code)
	return d

def download_stock_profit(year, quarter):
	d = get_stock_profit(year, quarter)
	if d.empty:
		return False
	if not os.path.isdir(STOCK_PROFIT_PATH):
		os.mkdir(STOCK_PROFIT_PATH)
	f_name = str(year) + '-' + str(quarter) + ".csv"
	f = os.path.join(STOCK_PROFIT_PATH, f_name)
	d.to_csv(f, index=False)
	return True

def download_all_stock_profit():
	yq = Time.getLastQuarter()
	ly = yq[0]
	lq = yq[1]
	for y in range(2010, ly):
		for q in range(1, 5):
			download_stock_profit(y, q)
	for q in range(1,lq+1):
		download_stock_profit(ly, q)
	return True

def download_latest_stock_profit():
	yq = Time.getLastQuarter()
	y = yq[0]
	q = yq[1]
	# 1st latest quarter
	download_stock_profit(y, q)
	# 2nd latest quarter
	if q == 1:
		download_stock_profit(y-1, 4)
	else:
		download_stock_profit(y, q-1)
	return True

def get_stock_growth(year, quarter):
	d = ts.get_growth_data(year, quarter)
	if type(d) == types.NoneType:
		return pd.DataFrame()
	d.loc[:,"code"] = d["code"].apply(Stock.norm_code)
	return d

def download_stock_growth(year, quarter):
	d = get_stock_growth(year, quarter)
	if d.empty:
		return False
	if not os.path.isdir(STOCK_GROWTH_PATH):
		os.mkdir(STOCK_GROWTH_PATH)
	f_name = str(year) + '-' + str(quarter) + ".csv"
	f = os.path.join(STOCK_GROWTH_PATH, f_name)
	d.to_csv(f, index=False)
	return True

def download_all_stock_growth():
	yq = Time.getLastQuarter()
	ly = yq[0]
	lq = yq[1]
	for y in range(2010, ly):
		for q in range(1, 5):
			download_stock_growth(y, q)
	for q in range(1,lq+1):
		download_stock_growth(ly, q)
	return True

def download_latest_stock_growth():
	yq = Time.getLastQuarter()
	y = yq[0]
	q = yq[1]
	# 1st latest quarter
	download_stock_growth(y, q)
	# 2nd latest quarter
	if q == 1:
		download_stock_growth(y-1, 4)
	else:
		download_stock_growth(y, q-1)
	return True

def get_stock_debt(year, quarter):
	d = ts.get_debtpaying_data(year, quarter)
	if type(d) == types.NoneType:
		return pd.DataFrame()
	d.loc[:,"code"] = d["code"].apply(Stock.norm_code)
	return d

def download_stock_debt(year, quarter):
	d = get_stock_debt(year, quarter)
	if d.empty:
		return False
	if not os.path.isdir(STOCK_DEBT_PATH):
		os.mkdir(STOCK_DEBT_PATH)
	f_name = str(year) + '-' + str(quarter) + ".csv"
	f = os.path.join(STOCK_DEBT_PATH, f_name)
	d.to_csv(f, index=False)
	return True

def download_all_stock_debt():
	yq = Time.getLastQuarter()
	ly = yq[0]
	lq = yq[1]
	for y in range(2010, ly):
		for q in range(1, 5):
			download_stock_debt(y, q)
	for q in range(1,lq+1):
		download_stock_debt(ly, q)
	return True

def download_latest_stock_debt():
	yq = Time.getLastQuarter()
	y = yq[0]
	q = yq[1]
	# 1st latest quarter
	download_stock_debt(y, q)
	# 2nd latest quarter
	if q == 1:
		download_stock_debt(y-1, 4)
	else:
		download_stock_debt(y, q-1)
	return True

def get_stock_cash(year, quarter):
	d = ts.get_cashflow_data(year, quarter)
	if type(d) == types.NoneType:
		return pd.DataFrame()
	d.loc[:,"code"] = d["code"].apply(Stock.norm_code)
	return d

def download_stock_cash(year, quarter):
	d = get_stock_cash(year, quarter)
	if d.empty:
		return False
	if not os.path.isdir(STOCK_CASH_PATH):
		os.mkdir(STOCK_CASH_PATH)
	f_name = str(year) + '-' + str(quarter) + ".csv"
	f = os.path.join(STOCK_CASH_PATH, f_name)
	d.to_csv(f, index=False)
	return True

def download_all_stock_cash():
	yq = Time.getLastQuarter()
	ly = yq[0]
	lq = yq[1]
	for y in range(2010, ly):
		for q in range(1, 5):
			download_stock_cash(y, q)
	for q in range(1,lq+1):
		download_stock_cash(ly, q)
	return True

def download_latest_stock_cash():
	yq = Time.getLastQuarter()
	y = yq[0]
	q = yq[1]
	# 1st latest quarter
	download_stock_cash(y, q)
	# 2nd latest quarter
	if q == 1:
		download_stock_cash(y-1, 4)
	else:
		download_stock_cash(y, q-1)
	return True

def get_stock_history(code):
	market = get_stock_market(code)
	if market == "unknown":
		return pd.DataFrame()
	url = stock_history_url_pattern.replace("CODE", code).replace("MARKET", market)
	try:
		f = Spider.openUrl(url)
		csv = pd.read_csv(f)
	except:
		Log.warning("failed to read '" + url + "'.")
		return pd.DataFrame()
	return csv

def get_stock_history_v2(code):
	df = ts.get_hist_data(code)
	if type(df) == types.NoneType:
		return pd.DataFrame()
	return df

def download_stock_history(code, path):
	d = get_stock_history(code)
	if d.empty:
		return False
	f = os.path.join(path, code+".csv")
	d.to_csv(f, index=False)
	return True

def download_stock_history_v2(code, path):
	d = get_stock_history_v2(code)
	if d.empty:
		return False
	f = os.path.join(path, code+".csv")
	d.to_csv(f)
	return True

def download_all_stock_history():
	stock_list_df = get_stock_list()
	if stock_list_df.empty:
		return False
	if not os.path.isdir(STOCK_HISTORY_PATH):
		os.mkdir(STOCK_HISTORY_PATH)
	for code in stock_list_df['Code']:
		download_stock_history(code, STOCK_HISTORY_PATH)
		time.sleep(2.5)
	return True

def download_all_stock_history_v2():
	stock_list_df = get_stock_basics()
	if stock_list_df.empty:
		return False
	if not os.path.isdir(STOCK_HISTORY_PATH):
		os.mkdir(STOCK_HISTORY_PATH)
	for code in stock_list_df.index:
		download_stock_history_v2(code, STOCK_HISTORY_PATH)
	return True

def download_all_index_history():
	if not os.path.isdir(INDEX_HISTORY_PATH):
		os.mkdir(INDEX_HISTORY_PATH)
	download_stock_history_v2('sh', INDEX_HISTORY_PATH)
	download_stock_history_v2('sz', INDEX_HISTORY_PATH)
	download_stock_history_v2('hs300', INDEX_HISTORY_PATH)
	download_stock_history_v2('sz50', INDEX_HISTORY_PATH)
	download_stock_history_v2('zxb', INDEX_HISTORY_PATH)
	download_stock_history_v2('cyb', INDEX_HISTORY_PATH)
	return True

if __name__ == '__main__':

#	#download_stock_list() # deprecated
#
#	download_stock_basics()
#
#	download_index_data()
#
#	download_stock_data()
#
#	download_all_stock_report() # once
#
#	download_latest_stock_report()
#
#	download_all_stock_profit() # once
#
#	download_latest_stock_profit()
#
#	download_all_stock_growth() # once
#
#	download_latest_stock_growth()
#
#	download_all_stock_debt() # once
#
#	download_latest_stock_debt()
#
	download_all_stock_cash() # once
#
#	download_latest_stock_cash()
#
#	download_all_index_history()
#
#	#download_all_stock_history()
#	download_all_stock_history_v2()
#
#	#download_all_stock_restoration_price() # todo

