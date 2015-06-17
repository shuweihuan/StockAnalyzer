#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.File import File
from base.Time import Time
from base.Stock import Stock

def get_stock_daily_incr():

	stock_history_path = STOCK_RESTORATION_HISTORY_PATH
	if not os.path.isdir(stock_history_path):
		return False
	stock_incr_path = STOCK_DAILY_INCR_DATA_PATH

	stock_basics = Stock.get_stock_basics()
	stock_list = stock_basics.index
	df = pd.DataFrame()
	for code in stock_list:
		stock_history_data_path = os.path.join(stock_history_path, code + ".csv")
		if not os.path.isfile(stock_history_data_path):
			continue
		stock_history_df = pd.read_csv(stock_history_data_path).sort_index(by="date")
		stock_history_df["code"] = code
		stock_history_df["name"] = stock_basics.ix[code, "name"]
		stock_incr_df = pd.DataFrame()
		stock_incr_df["code"] = stock_history_df["code"]
		stock_incr_df["name"] = stock_history_df["name"]
		stock_incr_df["date"] = stock_history_df["date"]
		stock_incr_df["incr1"] = stock_history_df["close"].pct_change(periods=1).shift(-1)
		stock_incr_df["incr3"] = stock_history_df["close"].pct_change(periods=3).shift(-3)
		stock_incr_df["incr5"] = stock_history_df["close"].pct_change(periods=5).shift(-5)
		stock_incr_df["incr10"] = stock_history_df["close"].pct_change(periods=10).shift(-10)
		stock_incr_df["incr20"] = stock_history_df["close"].pct_change(periods=20).shift(-20)
		stock_incr_df["incr60"] = stock_history_df["close"].pct_change(periods=60).shift(-60)
		df = df.append(stock_incr_df, ignore_index=True)
	df.to_csv(stock_incr_path, index=False)

	return True

def get_stock_quarterly_incr():

	stock_history_path = STOCK_RESTORATION_HISTORY_PATH
	if not os.path.isdir(stock_history_path):
		return False
	stock_incr_path = STOCK_QUARTERLY_INCR_DATA_PATH

	stock_basics = Stock.get_stock_basics()
	stock_list = stock_basics.index
	q_list = []
	attr_list = ["code", "name"]
	y, q = Time.getThisQuarter()
	q_list.append((y, q))
	attr_list.append(str(y) + '-' + str(q))
	for i in range(4):
		y, q = Time.getPrevQuarter(y, q)
		q_list.append((y, q))
		attr_list.append(str(y) + '-' + str(q))
	stock_incr_df = pd.DataFrame()
	for code in stock_list:
		stock_history_data_path = os.path.join(stock_history_path, code + ".csv")
		if not os.path.isfile(stock_history_data_path):
			continue
		stock_history_df = pd.read_csv(stock_history_data_path, index_col="date").sort_index()
		stock_incr_dict = {}
		stock_incr_dict["code"] = code
		stock_incr_dict["name"] = stock_basics.ix[code, "name"]
		for y, q in q_list:
			q_name = str(y) + '-' + str(q)
			thisqf = Time.getFirstDayOfQuarter(y, q)
			thisql = Time.getLastDayOfQuarter(y, q)
			block = stock_history_df[thisqf:thisql]
			if block.empty:
				stock_incr_dict[q_name] = np.nan
			else:
				stock_incr_dict[q_name] = block.iloc[-1]["close"] / block.iloc[0]["open"]
		stock_incr_df = stock_incr_df.append(stock_incr_dict, ignore_index=True)
		stock_incr_df = stock_incr_df.reindex(columns=attr_list)
	stock_incr_df.to_csv(stock_incr_path, index=False)
	return True
			
def get_stock_data_by_quarter(path, year, quarter):

	this_q_file_name = str(year) + "-" + str(quarter) + ".csv"
	this_q_file_path = os.path.join(path, this_q_file_name)
	if not os.path.isfile(this_q_file_path):
		return ()
	prev_q = Time.getPrevQuarter(year, quarter)
	prev_q_file_name = str(prev_q[0]) + "-" + str(prev_q[1]) + ".csv"
	prev_q_file_path = os.path.join(path, prev_q_file_name)
	if not os.path.isfile(prev_q_file_path):
		return ()
	this_q_df = pd.read_csv(this_q_file_path, dtype={"code":"object"})
	prev_q_df = pd.read_csv(prev_q_file_path, dtype={"code":"object"})
	return (this_q_df, prev_q_df)

def get_stock_fundholding_features(year, quarter):

	(this_q_df, prev_q_df) = get_stock_data_by_quarter(STOCK_FUNDHOLDING_PATH, year, quarter)
	this_q_df = this_q_df.drop(["date"], axis=1)
	this_q_df = this_q_df.rename(columns={"nlast":"nums_delta", "clast":"count_delta"})
	prev_q_df = prev_q_df.drop(["name", "date", "nlast", "clast"], axis=1)
	prev_q_df = prev_q_df.rename(columns={"nums":"prev_nums", "count":"prev_count", "amount":"prev_amount", "ratio":"prev_ratio"})
	df = pd.merge(this_q_df, prev_q_df, on="code", how="outer")
	df["nums_incr"] = df["nums"] / df["prev_nums"]
	df["count_incr"] = df["count"] / df["prev_count"]
	df["amount_delta"] = df["amount"] - df["prev_amount"]
	df["amount_incr"] = df["amount"] / df["prev_amount"]
	df["ratio_delta"] = df["ratio"] - df["prev_ratio"]
	df["ratio_incr"] = df["ratio"] / df["prev_ratio"]
	df = df.drop(["prev_nums", "prev_count", "prev_amount", "prev_ratio"], axis=1)
	df = df.reindex(columns=["code", "name", "nums", "nums_delta", "nums_incr", "count", "count_delta", "count_incr",
										 "amount", "amount_delta", "amount_incr", "ratio", "ratio_delta", "ratio_incr"])		
	return df

#def get_stock_profit_features(year, quarter):

	#(this_q_df, prev_q_df) = get_stock_data_by_quarter(STOCK_PROFIT_PATH, year, quarter)


if __name__ == "__main__":
	
	get_stock_daily_incr()
	#get_stock_quarterly_incr()
	#get_stock_fundholding_features(2015, 1).to_csv("stock_fundholding.2015-1.csv")

