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

def get_index_daily_incr():

	""" 获得所有指数历史每天的未来价格增长数据（用于预测/对比） """

	index_history_path = INDEX_HISTORY_PATH
	if not os.path.isdir(index_history_path):
		return False
	index_incr_path = INDEX_DAILY_INCR_DATA_PATH

	index_dict = {"sh":"上证指数", "sz":"深圳成指", "hs300":"沪深300", "cyb":"创业板", "zxb":"中小板", "sz50":"上证50"}
	df = pd.DataFrame()
	for code in index_dict.keys():
		index_history_data_path = os.path.join(index_history_path, code + ".csv")
		if not os.path.isfile(index_history_data_path):
			continue
		index_history_df = pd.read_csv(index_history_data_path).sort_index(by="date")
		index_history_df["code"] = code
		index_history_df["name"] = index_dict[code]
		index_incr_df = pd.DataFrame()
		index_incr_df["code"] = index_history_df["code"]
		index_incr_df["name"] = index_history_df["name"]
		index_incr_df["date"] = index_history_df["date"]
		index_incr_df["close"] = index_history_df["close"]
		index_incr_df["incr1"] = index_history_df["close"].pct_change(periods=1).shift(-1)
		index_incr_df["incr3"] = index_history_df["close"].pct_change(periods=3).shift(-3)
		index_incr_df["incr5"] = index_history_df["close"].pct_change(periods=5).shift(-5)
		index_incr_df["incr10"] = index_history_df["close"].pct_change(periods=10).shift(-10)
		index_incr_df["incr20"] = index_history_df["close"].pct_change(periods=20).shift(-20)
		index_incr_df["incr60"] = index_history_df["close"].pct_change(periods=60).shift(-60)
		df = df.append(index_incr_df, ignore_index=True)
	df.to_csv(index_incr_path, index=False)

	return True

def get_stock_daily_incr():

	""" 获得所有股票历史每天的未来价格增长数据（用于预测） """

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
		stock_incr_df["close"] = stock_history_df["close"]
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

	""" 获得所有股票历史上每季的价格增长数据 """

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
			
def get_stock_eps_quarterly_features(year, quarter, n=4):

	""" 获得所有股票最近n个季度的每股盈利（EPS）及同比增长 """

	eps_df = pd.DataFrame()
	(y, q) = (year, quarter)
	for i in range(n):
		(y, q) = Time.getPrevQuarter(y, q)
		q_name = str(y) + "-" + str(q)
		q_file_name = q_name + ".csv"
		q_file_path = os.path.join(STOCK_REPORT_PATH, q_file_name)
		if not os.path.isfile(q_file_path):
			continue
		q_df = pd.read_csv(q_file_path, dtype={"code":"object"})
		q_df = q_df[["code", "eps", "eps_yoy"]]
		q_df["eps"] = q_df["eps"].apply(Stock.norm_value).astype("float32")
		q_df["eps_yoy"] = q_df["eps_yoy"].apply(Stock.norm_value).astype("float32")
		q_df["eps_yoy"] = q_df["eps_yoy"] / 100
		q_df = q_df.rename(columns={"eps":"eps-q"+str(i), "eps_yoy":"eps_yoy-q"+str(i)})
		if eps_df.empty:
			eps_df = q_df
		else:
			eps_df = pd.merge(eps_df, q_df, on="code", how="outer")
	for i in range(n-1):
		eps_df["eps_yoy_incr-q"+str(i)] = ( eps_df["eps_yoy-q"+str(i)] - eps_df["eps_yoy-q"+str(i+1)] ) / eps_df["eps_yoy-q"+str(i+1)]
	return eps_df.set_index("code")

def get_stock_eps_yearly_features(year, n=3):

	""" 获得所有股票最近n个年度的每股盈利（EPS）及增长 """

	eps_df = pd.DataFrame()
	y = year
	for i in range(n):
		y = Time.getPrevYear(y)
		y_name = str(y)
		q_name = str(y) + "-4"
		q_file_name = q_name + ".csv"
		q_file_path = os.path.join(STOCK_REPORT_PATH, q_file_name)
		if not os.path.isfile(q_file_path):
			continue
		q_df = pd.read_csv(q_file_path, dtype={"code":"object"})
		q_df = q_df[["code", "eps"]]
		q_df["eps"] = q_df["eps"].apply(Stock.norm_value).astype("float32")
		q_df = q_df.rename(columns={"eps":"eps-y"+str(i)})
		if eps_df.empty:
			eps_df = q_df
		else:
			eps_df = pd.merge(eps_df, q_df, on="code", how="outer")
	for i in range(n-1):
		eps_df["eps_yoy-y"+str(i)] = ( eps_df["eps-y"+str(i)] - eps_df["eps-y"+str(i+1)] ) / eps_df["eps-y"+str(i+1)]
	for i in range(n-2):
		eps_df["eps_yoy_incr-y"+str(i)] = ( eps_df["eps_yoy-y"+str(i)] - eps_df["eps_yoy-y"+str(i+1)] ) / eps_df["eps_yoy-y"+str(i+1)]
	return eps_df.set_index("code")

def get_stock_roe_yearly_features(year, n=3):

	""" 获得所有股票最近n个年度的净资产收益率（ROE）及增长 """

	roe_df = pd.DataFrame()
	y = year
	for i in range(n):
		y = Time.getPrevYear(y)
		y_name = str(y)
		q_name = str(y) + "-4"
		q_file_name = q_name + ".csv"
		q_file_path = os.path.join(STOCK_REPORT_PATH, q_file_name)
		if not os.path.isfile(q_file_path):
			continue
		q_df = pd.read_csv(q_file_path, dtype={"code":"object"})
		q_df = q_df[["code", "roe"]]
		q_df["roe"] = q_df["roe"].apply(Stock.norm_value).astype("float32")
		q_df = q_df.rename(columns={"roe":"roe-y"+str(i)})
		if roe_df.empty:
			roe_df = q_df
		else:
			roe_df = pd.merge(roe_df, q_df, on="code", how="outer")
	for i in range(n-1):
		roe_df["roe_yoy-y"+str(i)] = ( roe_df["roe-y"+str(i)] - roe_df["roe-y"+str(i+1)] ) / roe_df["roe-y"+str(i+1)]
	for i in range(n-2):
		roe_df["roe_yoy_incr-y"+str(i)] = ( roe_df["roe_yoy-y"+str(i)] - roe_df["roe_yoy-y"+str(i+1)] ) / roe_df["roe_yoy-y"+str(i+1)]
	return roe_df.set_index("code")

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

if __name__ == "__main__":
	
	get_index_daily_incr()
	#get_stock_daily_incr()
	#get_stock_quarterly_incr()
	#get_stock_fundholding_features(2015, 1).to_csv("stock_fundholding.2015-1.csv")
#	q_eps_df = get_stock_eps_quarterly_features(2015,2).reset_index()
#	y_eps_df = get_stock_eps_yearly_features(2015).reset_index()
#	eps_df = pd.merge(q_eps_df, y_eps_df, on="code", how="outer")
#	eps_df = eps_df.set_index("code")
#	eps_df.to_csv("all.csv")
#	eps_df = eps_df[ (eps_df["eps_yoy-q0"] > 0.2) & (eps_df["eps_yoy-q1"] > 0.2) ] 
#	eps_df = eps_df[ (eps_df["eps_yoy-y0"] > 0.2) & (eps_df["eps_yoy-y1"] > 0.2) ]
#	#eps_df = eps_df[ (eps_df["eps_yoy_incr-q0"] > 0) ]
#	eps_df = eps_df[ (eps_df["eps_yoy_incr-y0"] > 0) ]
#	eps_df.to_csv("canslim.csv")
#
#	y_roe_df = get_stock_eps_yearly_features(2015).reset_index()
#	y_roe_df.to_csv("roe.csv")
