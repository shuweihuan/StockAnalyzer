#!/usr/bin/python
#coding: utf-8

import os
import sys
import time
import types
import numpy as np
import pandas as pd
import tushare as ts
sys.path.append("../..")
from conf.config import *

class Stock:

	@staticmethod
	def norm_code(code):
		code = str(code)
		l = 6 - len(code)
		return '0' * l + code

	@staticmethod
	def is_code(code):
		code = Stock.norm_code(code)
		if len(code) != 6:
			return False
		if code[:2] == "60" or code[:2] == "00" or code[:2] == "30":
			return True
		return False

	@staticmethod
	def get_market(code):
		code = Stock.norm_code(code)
		if len(code) == 6:
			if code[:2] == "60":
				return "sh"
			if code[:2] == "00" or code[:2] == "30":
				return "sz"
		return "unknown"
	
	@staticmethod
	def get_code_list():
		stock_list_csv_path = STOCK_BASICS_DATA_PATH
		if os.path.isfile(stock_list_csv_path):
			stock_list_df = pd.read_csv(stock_list_csv_path, dtype={"code":"object"})
		else:
			stock_list_df = ts.get_stock_basics()
		return stock_list_df["code"]
	
	@staticmethod
	def get_stock_basics():
		stock_basics_csv_path = STOCK_BASICS_DATA_PATH
		if os.path.isfile(stock_basics_csv_path):
			stock_basics_df = pd.read_csv(stock_basics_csv_path, dtype={"code":"object"})
			stock_basics_df = stock_basics_df.set_index("code")
		else:
			stock_basics_df = ts.get_stock_basics()
		return stock_basics_df

