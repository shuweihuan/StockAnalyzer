#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd

def get_stock_features(code, price_history):
	data = price_history.copy()
	data['Adj Open'] = price_history['Adj Close'] / price_history['Close'] * price_history['Open']
	data['Adj High'] = price_history['Adj Close'] / price_history['Close'] * price_history['High']
	data['Adj Low'] = price_history['Adj Close'] / price_history['Close'] * price_history['Low']
	for i in range(10):
		key = 'Lag ' + str(i)
		data[key] = 


if __name__ == "__main__":
	code = "600000"
	price_history_file = "/root/workspace/StockAnalyzer/data/stock_price_history/600000.csv"
	price_history = pd.read_csv(price_history_file)
	get_stock_features(code, price_history)

