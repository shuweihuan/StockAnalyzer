#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
from get_stock_features import *
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.Log import Log
from base.File import File
from base.Time import Time
from base.Stock import Stock

def get_stock_incr_by_quarter(year, quarter):

	stock_list = Stock.get_code_list()
	df = pd.DataFrame()
	stock_history_path = STOCK_RESTORATION_HISTORY_PATH
	if not os.path.isdir(stock_history_path):
		return df
	for code in stock_list:
		stock_history_csv_path = os.path.join(stock_history_path, code + ".csv")
		if not os.path.isfile(stock_history_csv_path):
			Log.warning("file '" + stock_history_csv_path + "' does not exist.")
			continue
		stock_history_df = pd.read_csv(stock_history_csv_path)
		q_first_date = Time.getFirstDayOfQuarter(year, quarter)
		q_last_date = Time.getLastDayOfQuarter(year, quarter)
		q_range = stock_history_df[(stock_history_df["date"] >= q_first_date) & (stock_history_df["date"] <= q_last_date)]
		if q_range.empty:
			continue
		q_range = q_range.sort_index(by="date")
		incr = q_range.iloc[-1]["close"] / q_range.iloc[0]["open"]
		df = df.append({"code":code, "incr":incr}, ignore_index=True)

	return df

def get_stock_training_by_quarter(year, quarter):

	stock_incr_df = get_stock_incr_by_quarter(year, quarter)
	pq = Time.getPrevQuarter(year, quarter)
	y = pq[0]
	q = pq[1]
	stock_fundholding_df = get_stock_fundholding_features(y, q).drop("name", axis=1)
	df = stock_incr_df
	df = pd.merge(df, stock_fundholding_df, on="code", how="outer")

	return df 

if __name__ == "__main__":

	train_df = get_stock_training_by_quarter(2015,1).dropna(axis=0)
	#test_df = get_stock_training_by_quarter(2015,2) 

	print train_df.head()
	train_X = train_df[["nums", "nums_delta", "nums_incr", "count", "count_delta", "count_incr"]].values.astype("float32")
	train_y = train_df["incr"].values.astype("float32")
	print type(train_X)
	print type(train_y)

	est = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0, loss='ls').fit(train_X, train_y)
	mse = mean_squared_error(train_y, est.predict(train_X))    
	print mse

