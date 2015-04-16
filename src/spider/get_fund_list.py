#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import string
import urllib2
import re
from bs4 import BeautifulSoup

all_funds_value_url = "http://www.howbuy.com/board/"
stock_funds_value_url = "http://www.howbuy.com/board/gupiao.htm"
hybrid_funds_value_url = "http://www.howbuy.com/board/hunhe.htm"
index_funds_value_url = "http://www.howbuy.com/board/zhishu.htm"

all_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/"
stock_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/gupiao.htm"
hybrid_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/hunhe.htm"
index_funds_ranking_url = "http://www.howbuy.com/fund/fundranking/zhishu.htm"

fund_url_prefix = "http://www.howbuy.com/fund/"

def get_html(url):
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0')
	opener = urllib2.build_opener()
	html = opener.open(request).read()
	return html

def get_list_info_date():
	url = "http://www.howbuy.com/board/"
	html = get_html(url)
	soup = BeautifulSoup(html)
	list_info = soup.find('div', class_='dataTables').find('div', class_='quotation')
	list_info_text = list_info.get_text().encode('utf-8')
	list_info_date = re.search(r'(\d+)-(\d+)-(\d+)', list_info_text).group(0).replace('-','')
	return list_info_date

def get_value_list_data(url, fout):
	html = get_html(url)
	soup = BeautifulSoup(html)
	fout.write("#Rank\tCode\tName\tUnit.Value\tAcc.Value\tPrev.UnitValue\tPrev.Acc.Value\tIncrease\tIncrease.Rate\n")
	list_data = soup.find('div', class_='dataTables').find('div', 'result_list')
	tr_list = list_data.find_all('tr')
	for tr in tr_list:
		s = ""
		td_list = tr.find_all('td')
		if len(td_list) != 11:
			continue
		for td in td_list[1:10]:
			s += td.get_text().encode('utf-8')
			s += "\t"
		fout.write(s.strip() + "\n")

def get_ranking_list_data(url, fout):
	html = get_html(url)
	soup = BeautifulSoup(html)
	fout.write("#Rank\tCode\tName\tDate\tValue\tWeekly.Yield\tMonthly.Yield\tQuarterly.Yield\tHalf.Year.Yield\tYear.Yield\tThis.Year.Yield\n")
	list_data = soup.find('div', class_='dataTables').find('div', 'result_list')
	tr_list = list_data.find_all('tr')
	for tr in tr_list:
		s = ""
		td_list = tr.find_all('td')
		if len(td_list) != 14:
			continue
		for td in td_list[1:12]:
			s += td.get_text().encode('utf-8')
			s += "\t"
		fout.write(s.strip() + "\n")

def get_stock_position(code):
	url = fund_url_prefix + code
	html = get_html(url)
	soup = BeautifulSoup(html)
	stock_rate = ""
	stock_rate_box = soup.find('span', id='calcTopGp')
	if stock_rate_box:
		stock_rate = stock_rate_box.get_text().encode('utf-8')
	if stock_rate == "" :
		return [] 
	stock_date = ""
	stock_date_box = soup.find('select', id='selDate_zccg')
	if stock_date_box:
		stock_date = stock_date_box.option.get_text().encode('utf-8')
	if stock_date == "":
		return []
	stock_list_box = soup.find('div', id='content')
	if stock_list_box:
		stock_list = stock_list_box.find_all('tr')
		l = []
		for tr in stock_list[1:]:
			s = ""
			td_list = tr.find_all('td')
			if len(td_list) != 5:
				continue
			for td in td_list:
				s += td.get_text().encode('utf-8')
				s += "\t"
			s = s.strip()
			l.append(stock_rate + "\t" + stock_date + "\t" + s)
		return l
	else:
		return []

if __name__ == '__main__':
	
	# environment
	date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	data_path = "data"
	if not os.path.isdir(data_path):
		os.mkdir(data_path)
	info_date = get_list_info_date()
	info_date_no_dash = info_date.replace('-', '')

#	# get all funds value
#	data_file = os.path.join(data_path, "all_funds_value." + info_date_no_dash + ".data")
#	if os.path.isfile(data_file):
#		sys.stderr.write("warning: file '" + data_file + "' exists.\n")
#	fout = open(data_file, 'w')
#	get_value_list_data(all_funds_value_url, fout)	
#	fout.close()
#
#	# get all funds ranking
#	data_file = os.path.join(data_path, "all_funds_ranking." + info_date_no_dash + ".data")
#	if os.path.isfile(data_file):
#		sys.stderr.write("warning: file '" + data_file + "' exists.\n")
#	fout = open(data_file, 'w')
#	get_ranking_list_data(all_funds_ranking_url, fout)	
#	fout.close()
#
	# get stock funds value
	stock_funds_value_data_file = os.path.join(data_path, "stock_funds_value." + info_date_no_dash + ".data")
	if os.path.isfile(stock_funds_value_data_file):
		sys.stderr.write("warning: file '" + stock_funds_value_data_file + "' exists.\n")
	fout = open(stock_funds_value_data_file, 'w')
	get_value_list_data(stock_funds_value_url, fout)	
	fout.close()
	
	# get stock funds ranking
	stock_funds_ranking_data_file = os.path.join(data_path, "stock_funds_ranking." + info_date_no_dash + ".data")
	if os.path.isfile(stock_funds_ranking_data_file):
		sys.stderr.write("warning: file '" + stock_funds_ranking_data_file + "' exists.\n")
	fout = open(stock_funds_ranking_data_file, 'w')
	get_ranking_list_data(stock_funds_ranking_url, fout)	
	fout.close()

	# get stock position
#	data_file = os.path.join(data_path, "stock_position." + info_date_no_dash + ".data")
#	if os.path.isfile(data_file):
#		sys.stderr.write("warning: file '" + data_file + "' exists.\n")
#	fout = open(data_file, 'w')
#	fin = open(stock_funds_value_data_file, 'r')
#	for line in fin:
#		line = line.strip()
#		if line.startswith('#'):
#			continue
#		f = line.split("\t")
#		code = f[1]
#		name = f[2]
#		stock_position_list = get_stock_position(code)
#		for s in stock_position_list:
#			print code + " " + name + " " + s
#		break
#	fin.close()
#	fout.close()

