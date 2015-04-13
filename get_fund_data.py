#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import string
import urllib2
import re
from bs4 import BeautifulSoup

fund_short_term_url = "http://www.howbuy.com/board/"
fund_long_term_url = "http://www.howbuy.com/fund/fundranking/"

def get_html(url):
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0')
	opener = urllib2.build_opener()
	html = opener.open(request).read()
	return html

def get_short_term_info(url, fout):
	html = get_html(url)
	soup = BeautifulSoup(html)
	fund_info = soup.find('div', class_='dataTables').find('div', class_='quotation')
	fund_info_text = fund_info.get_text().encode('utf-8')
	fund_info_date = re.search(r'(\d+)-(\d+)-(\d+)', fund_info_text).group(0).replace('-','')
	data_file = os.path.join(data_path, "short-term." + fund_info_date + '.data')
	if os.path.isfile(data_file):
		sys.stderr.write("warning: file '" + data_file + "' exists.\n")
	fout.write("#Rank\tCode\tName\tUnit.Value\tAcc.Value\tPrev.UnitValue\tPrev.Acc.Value\tIncrease\tIncrease.Rate\n")
	fund_data = soup.find('div', class_='dataTables').find('div', 'result_list')
	tr_list = fund_data.find_all('tr')
	for tr in tr_list:
		s = ""
		td_list = tr.find_all('td')
		if len(td_list) != 11:
			continue
		for td in td_list[1:10]:
			s += td.get_text().encode('utf-8')
			s += "\t"
		fout.write(s.strip() + "\n")

def get_long_term_info(url, fout):
	html = get_html(url)
	soup = BeautifulSoup(html)
	fund_info = soup.find('div', class_='dataTables').find('div', class_='quotation')
	fund_info_text = fund_info.get_text().encode('utf-8')
	fund_info_date = re.search(r'(\d+)-(\d+)-(\d+)', fund_info_text).group(0).replace('-','')
	data_file = os.path.join(data_path, "long-term." + fund_info_date + '.data')
	if os.path.isfile(data_file):
		sys.stderr.write("warning: file '" + data_file + "' exists.\n")
	fout.write("#Rank\tCode\tName\tDate\tValue\tWeekly.Yield\tMonthly.Yield\tQuarterly.Yield\tHalf.Year.Yield\tYear.Yield\tThis.Year.Yield\n")
	fund_data = soup.find('div', class_='dataTables').find('div', 'result_list')
	tr_list = fund_data.find_all('tr')
	for tr in tr_list:
		s = ""
		td_list = tr.find_all('td')
		if len(td_list) != 14:
			continue
		for td in td_list[1:11]:
			s += td.get_text().encode('utf-8')
			s += "\t"
		fout.write(s.strip() + "\n")

if __name__ == '__main__':
	
	# environment
	date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	data_path = 'data'
	if not os.path.isdir(data_path):
		os.mkdir(data_path)

	# get short-term funds data
	soup = BeautifulSoup(html)
	fund_info = soup.find('div', class_='dataTables').find('div', class_='quotation')
	fund_info_text = fund_info.get_text().encode('utf-8')
	fund_info_date = re.search(r'(\d+)-(\d+)-(\d+)', fund_info_text).group(0).replace('-','')
	data_file = os.path.join(data_path, "short-term." + fund_info_date + '.data')
	if os.path.isfile(data_file):
		sys.stderr.write("warning: file '" + data_file + "' exists.\n")
	fout = open(data_file, 'w')
	fout.write("#Rank\tCode\tName\tUnit.Value\tAcc.Value\tPrev.UnitValue\tPrev.Acc.Value\tIncrease\tIncrease.Rate\n")
	fund_data = soup.find('div', class_='dataTables').find('div', 'result_list')
	tr_list = fund_data.find_all('tr')
	for tr in tr_list:
		s = ""
		td_list = tr.find_all('td')
		if len(td_list) != 11:
			continue
		for td in td_list[1:10]:
			s += td.get_text().encode('utf-8')
			s += "\t"
		fout.write(s.strip() + "\n")
	fout.close()

	# get long-term fund data
	html = get_html(fund_long_term_url)
	soup = BeautifulSoup(html)
	fund_info = soup.find('div', class_='dataTables').find('div', class_='quotation')
	fund_info_text = fund_info.get_text().encode('utf-8')
	fund_info_date = re.search(r'(\d+)-(\d+)-(\d+)', fund_info_text).group(0).replace('-','')
	data_file = os.path.join(data_path, "long-term." + fund_info_date + '.data')
	if os.path.isfile(data_file):
		sys.stderr.write("warning: file '" + data_file + "' exists.\n")
	fout = open(data_file, 'w')
	fout.write("#Rank\tCode\tName\tDate\tValue\tWeekly.Yield\tMonthly.Yield\tQuarterly.Yield\tHalf.Year.Yield\tYear.Yield\tThis.Year.Yield\n")
	fund_data = soup.find('div', class_='dataTables').find('div', 'result_list')
	tr_list = fund_data.find_all('tr')
	for tr in tr_list:
		s = ""
		td_list = tr.find_all('td')
		if len(td_list) != 14:
			continue
		for td in td_list[1:11]:
			s += td.get_text().encode('utf-8')
			s += "\t"
		fout.write(s.strip() + "\n")
	fout.close()
    
	# get fund code list
	fin = open(data_file, 'r')
	for line in fin:
		line = line.strip()
		if line.startswith('#'):
			continue
		f = line.split("\t")
		code = f[1]
		name = f[2]
		url = "http://www.howbuy.com/fund/" + code
		html = get_html(url)
		stock_rate = ""
		soup = BeautifulSoup(html)
		stock_rate_box = soup.find('span', id='calcTopGp')
		if stock_rate_box:
			stock_rate = stock_rate_box.get_text().encode('utf-8')
		if stock_rate == "" :
			continue
		stock_date = ""
		stock_date_box = soup.find('select', id='selDate_zccg')
		if stock_date_box:
			stock_date = stock_date_box.option.get_text().encode('utf-8')
		if stock_date == "":
			continue
		stock_list_box = soup.find('div', id='content')
		if stock_list_box:
			stock_list = stock_list_box.find_all('tr')
			for tr in stock_list[1:]:
				s = ""
				td_list = tr.find_all('td')
				if len(td_list) != 5:
				for td in td_list:
					s += td.get_text().encode('utf-8')
					s += "\t"
				s = s.strip()
				print code + " " + name + " " + stock_date + " " + stock_rate + " " + s
	fin.close()

