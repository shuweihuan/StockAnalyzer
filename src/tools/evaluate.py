#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
sys.path.append("../..")
from conf.config import *

def evaluate_daily_strategy(strategy_code):

	stock_daily_incr_file = STOCK_DAILY_INCR_DATA_PATH
	if not os.path.isfile(stock_daily_incr_file):
		return False
	stock_daily_incr_df = pd.read_csv(stock_daily_incr_file, dtype={"code":"object"})
	index_daily_incr_file = INDEX_DAILY_INCR_DATA_PATH
	if not os.path.isfile(index_daily_incr_file):
		return False
	index_daily_incr_df = pd.read_csv(index_daily_incr_file, dtype={"code":"object"})

	strategy_eval_path = STRATEGY_EVAL_PATH
	if not os.path.isdir(strategy_eval_path):
		return False
	strategy_out_file = os.path.join(strategy_eval_path, strategy_code + ".out.csv")
	strategy_eval_file = os.path.join(strategy_eval_path, strategy_code + ".eval.csv")
	strategy_desc_file = os.path.join(strategy_eval_path, strategy_code + ".desc.csv")
	strategy_index_eval_file = os.path.join(strategy_eval_path, strategy_code + ".index.eval.csv")
	strategy_index_desc_file = os.path.join(strategy_eval_path, strategy_code + ".index.desc.csv")

	strategy_out_df = pd.read_csv(strategy_out_file, dtype={"code":"object"})
	strategy_eval_df = pd.merge(strategy_out_df, stock_daily_incr_df, on=["code", "date"], how="left").set_index(["code","name","date"])
	strategy_eval_df.to_csv(strategy_eval_file)
	strategy_desc_df = strategy_eval_df.describe()
	strategy_desc_df.to_csv(strategy_desc_file)
	index_list = ["sh", "sz", "hs300", "cyb", "zxb", "sz50"]
	strategy_index_out_df = pd.DataFrame()
	for code in index_list:
		temp_df = strategy_out_df.copy()
		temp_df["code"] = code
		strategy_index_out_df = strategy_index_out_df.append(temp_df, ignore_index=True)
	strategy_index_eval_df = pd.merge(strategy_index_out_df, index_daily_incr_df, on=["code", "date"], how="left")
	strategy_index_eval_df.set_index(["code","name","date"]).to_csv(strategy_eval_file)
	strategy_index_desc_df = strategy_index_eval_df.groupby(["code","name"]).describe()
	strategy_index_desc_df.to_csv(strategy_index_desc_file)

	return True

if __name__ == "__main__":

	evaluate_daily_strategy("s001")
	
