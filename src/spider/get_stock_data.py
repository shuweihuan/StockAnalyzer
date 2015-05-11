#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import string
import shutil
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
sys.path.append("..")
from base.Log import Log
from base.Spider import Spider

stock_list_url = "http://quote.eastmoney.com/stocklist.html"
stock_price_history_url_pattern = "http://table.finance.yahoo.com/table.csv?s=CODE.MARKET"

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

def download_stock_list(path):
	d = get_stock_list()
	d.to_csv(path)
	return True

def get_stock_price_history(code):
	market = get_stock_market(code)
	if market == "unknown":
		return pd.DataFrame()
	url = stock_price_history_url_pattern.replace("CODE", code).replace("MARKET", market)
	try:
		f = Spider.openUrl(url)
		csv = pd.read_csv(f)
	except:
		Log.warning("failed to read '" + url + "'.")
		return pd.DataFrame()
	return csv

def download_stock_price_history(code, path):
	d = get_stock_price_history(code)
	if d.empty:
		return False
	f = os.path.join(path, code+".csv")
	d.to_csv(f)
	return True

def download_all_stock_price_history(path):
	stock_list_df = get_stock_list()
	for code in stock_list_df['Code']:
		download_stock_price_history(code, path)
		time.sleep(2)
	return True

if __name__ == '__main__':

	if len(sys.argv) != 2:
		msg = "invalid arguments: "
		msg += " ".join(sys.argv)
		msg += "."
		Log.error(msg)
		sys.exit(1)

	data_path = sys.argv[1]

	if not os.path.isdir(data_path):
		os.mkdir(data_path)

	# download stock list
	stock_list_path = os.path.join(data_path, "stock_list.csv")
	stock_list_bak_path = os.path.join(data_path, "stock_list.bak.csv")
	if os.path.isfile(stock_list_path):
		if os.path.isfile(stock_list_bak_path):
			os.remove(stock_list_bak_path)
		os.rename(stock_list_path, stock_list_bak_path)
	download_stock_list(stock_list_path)

	# download stock price history
	stock_price_history_path = os.path.join(data_path, 'stock_price_history')
	stock_price_history_bak_path = os.path.join(data_path, 'stock_price_history.bak')
	if os.path.isdir(stock_price_history_path):
		if os.path.isdir(stock_price_history_bak_path):
			shutil.rmtree(stock_price_history_bak_path)
		os.rename(stock_price_history_path, stock_price_history_bak_path)
	os.mkdir(stock_price_history_path)
	download_all_stock_price_history(stock_price_history_path)

