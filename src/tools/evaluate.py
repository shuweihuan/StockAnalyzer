#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
sys.path.append("../..")
from conf.config import *

def evaluate_daily_strategy(strategy_csv, eval_csv):

	daily_incr_file = STOCK_DAILY_INCR_DATA_PATH
	if not os.path.isfile(daily_incr_file):
		return False
	daily_incr_df = pd.read_csv(daily_incr_file, dtype={"code":"object"})
	strategy_out_df = pd.read_csv(strategy_csv, dtype={"code":"object"})
	df = pd.merge(strategy_out_df, daily_incr_df, on=["code", "date"], how="left").set_index(["code","name","date"])
	df.to_csv(eval_csv)
	df_desc = df.describe()
	print df_desc

	return True

if __name__ == "__main__":

	evaluate_daily_strategy("test_in.csv", "test_out.csv")
	
