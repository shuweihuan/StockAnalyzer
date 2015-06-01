#!/usr/bin/python
#coding: utf-8

import os
import sys
import string
import numpy as np
import pandas as pd
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.Log import Log
from base.File import File

def norm_stock_name(x):

	return x.replace(" ", "")

def get_stock_funds_position():

	if not os.path.isfile(FUND_INFO_DATA_PATH):
		return pd.DataFrame()
	if not os.path.isdir(FUND_TOP_STOCK_PATH):
		return pd.DataFrame()

	fund_info_df = pd.read_csv(FUND_INFO_DATA_PATH, dtype={"Code":"object"})
	this_fund_top_stock_file = File.getLatestFilePath(FUND_TOP_STOCK_PATH)
	prev_fund_top_stock_file = File.getLatestFilePath(FUND_TOP_STOCK_PATH, n=2)
	this_fund_top_stock_df = pd.read_csv(this_fund_top_stock_file, dtype={"Code":"object"})
	prev_fund_top_stock_df = pd.read_csv(prev_fund_top_stock_file, dtype={"Code":"object"})

	del prev_fund_top_stock_df["Stock Price"]
	del prev_fund_top_stock_df["Stock Increase"]
	prev_fund_top_stock_df = prev_fund_top_stock_df.rename(columns={"Stock Volume" : "Prev Stock Volume", "Stock Position" : "Prev Stock Position"})
	fund_top_stock_df = pd.merge(this_fund_top_stock_df, prev_fund_top_stock_df, on=["Code", "Stock Name"], how="outer")
	fund_top_stock_df["Stock Volume Diff"] = fund_top_stock_df["Stock Volume"] - fund_top_stock_df["Prev Stock Volume"]
	fund_top_stock_df["Stock Position Diff"] = fund_top_stock_df["Stock Position"] - fund_top_stock_df["Prev Stock Position"]

	stock_fund_info_df = fund_info_df[fund_info_df['Type'].isin(["stock", "hybrid"])]
	stock_fund_position_df = pd.merge(stock_fund_info_df, fund_top_stock_df, on="Code", how="inner")
	stock_fund_position_df["Stock Name"] = stock_fund_position_df["Stock Name"].apply(norm_stock_name)
	return stock_fund_position_df.reindex(columns=[	"Code", "Name", "Type", "Daily Yield", "Weekly Yield", "Monthly Yield", "Quarterly Yield", "Half-yearly Yield", "Yearly Yield",
													"Stock Name", "Stock Price", "Stock Increase", "Stock Volume", "Stock Position",
													"Prev Stock Volume", "Prev Stock Position", "Stock Volume Diff", "Stock Position Diff"	])
													
def output_stock_funds_postion():

	if not os.path.isdir(FUND_STOCK_POSITION_PATH):
		os.mkdir(FUND_STOCK_POSITION_PATH)
	file_path = os.path.join(FUND_STOCK_POSITION_PATH, "stock_position.csv")

	fund_stock_df = get_stock_funds_position()
	if fund_stock_df.empty:
		return False
	fund_stock_df.to_csv(file_path, index=False)
	return True

def output_top_funds_position(n=25):

	if not os.path.isdir(FUND_STOCK_POSITION_PATH):
		os.mkdir(FUND_STOCK_POSITION_PATH)

	fund_stock_df = get_stock_funds_position()
	if fund_stock_df.empty:
		return False
	for c in ["Daily Yield", "Weekly Yield", "Monthly Yield", "Quarterly Yield", "Half-yearly Yield", "Yearly Yield"]:
		top_fund_list = fund_stock_df.sort_index(by=c, ascending=False)['Code'].drop_duplicates().head(n)
		top_fund_stock_df = fund_stock_df[fund_stock_df['Code'].isin(top_fund_list)].sort_index(by=c, ascending=False)
		file_name = "top_fund_stock_position." + c.replace(' ','') + ".csv"
		file_path = os.path.join(FUND_STOCK_POSITION_PATH, file_name)
		top_fund_stock_df.to_csv(file_path, index=False)
	return True

def stat_stock_position():

	fund_top_stock_df = get_stock_funds_position()
	stock_group_df = fund_top_stock_df.groupby("Stock Name")

	count = stock_group_df["Stock Position"].count()
	prev_count = stock_group_df["Prev Stock Position"].count()
	count_diff = count - prev_count
	volume = stock_group_df["Stock Volume"].sum()
	prev_volume = stock_group_df["Prev Stock Volume"].sum()
	volume_diff = volume - prev_volume
	volume_diff_rate = volume_diff / prev_volume
	position = stock_group_df["Stock Position"].mean()
	prev_position = stock_group_df["Prev Stock Position"].mean()

	stock_stat_df = pd.DataFrame({	"Count" : count,
									"Prev Count" : prev_count,
									"Count Diff" : count_diff,
									"Volume" : volume,
									"Prev Volume" : prev_volume,
									"Volume Diff" : volume_diff,
									"Volume Diff Rate" : volume_diff_rate,
									"Position" : position,
									"Prev Position" : prev_position	})
	stock_stat_df = stock_stat_df.reindex(columns = ["Count", "Prev Count", "Count Diff", "Volume", "Prev Volume", "Volume Diff", "Volume Diff Rate", "Position", "Prev Position"])

	for c in ["Daily Yield", "Weekly Yield", "Monthly Yield", "Quarterly Yield", "Half-yearly Yield", "Yearly Yield"]:
		file_name = "top_fund_stock_position." + c.replace(' ','') + ".csv"
		file_path = os.path.join(FUND_STOCK_POSITION_PATH, file_name)
		top_fund_stock_df = pd.read_csv(file_path, dtype={"Code" : "object"})
		groupby_df = top_fund_stock_df.groupby("Stock Name")
		attr_name = c + " Count"
		attr_value = groupby_df["Code"].count()
		stock_stat_df[attr_name] = attr_value
		attr_name = c + " Average Position"
		attr_value = groupby_df["Stock Position"].sum() / groupby_df["Code"].count()
		stock_stat_df[attr_name] = attr_value
		attr_name = c + " Max Position"
		attr_value = groupby_df["Stock Position"].max()
		stock_stat_df[attr_name] = attr_value

	return stock_stat_df

def output_stock_position_stat():

	if not os.path.isdir(FUND_STOCK_POSITION_PATH):
		os.mkdir(FUND_STOCK_POSITION_PATH)
	file_path = os.path.join(FUND_STOCK_POSITION_PATH, "stock_position_stat.csv")

	stat_df = stat_stock_position()
	stat_df.to_csv(file_path)

if __name__ == "__main__":
	
	output_stock_funds_postion()

	output_top_funds_position(n=25)

	output_stock_position_stat()

