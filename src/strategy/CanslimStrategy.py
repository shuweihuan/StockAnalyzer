#!/usr/bin/python
#coding: utf-8

###########
# CANSLIM #
###########

import os
import sys
import string
import numpy as np
import pandas as pd
from DailyStrategy import DailyStrategy
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.Log import Log
from base.Time import Time
from base.Data import Data
from base.File import File
from base.Stock import Stock
from analyzer.analyze_stock_data import *

class CanslimStrategy(DailyStrategy):

	def calc(self, time):
		y, q = Time.getThisQuarter(time)
		df = Stock.get_stock_info().reset_index()
		y_eps_df = get_stock_eps_yearly_features(y).reset_index()
		df = pd.merge(df, y_eps_df, on="code", how="outer")
		q_eps_df = get_stock_eps_quarterly_features(y, q).reset_index()
		df = pd.merge(df, q_eps_df, on="code", how="outer")
		df = df.set_index("code")
	
		# 近两年eps增长率大于20%
		df = df[ ( (df["eps_yoy-y0"] > 0.2) & (df["eps_yoy-y1"] > 0.2) ) | ( (np.isnan(df["eps_yoy-y0"])) & (df["eps_yoy-y1"] > 0.2) ) ]
		# 近两季度eps同比增长率大于20%
		df = df[ ( (df["eps_yoy-q0"] > 0.2) & (df["eps_yoy-q1"] > 0.2) ) | ( (np.isnan(df["eps_yoy-q0"])) & (df["eps_yoy-q1"] > 0.2) ) ]
		# 上年eps加速增长
		df = df[ (df["eps_yoy_incr-y0"] > 0) | (np.isnan(df["eps_yoy_incr-y0"])) ]
		# 上季度eps加速增长
		df = df[ (df["eps_yoy_incr-q0"] > 0) | (np.isnan(df["eps_yoy_incr-q0"])) ]

		# 格式优化
		df = df[["name", "changepercent", "turnoverratio", "pe", "industry", "concept" ]]
		df["changepercent"] = df["changepercent"].apply(Data.formatPercentage, keep=True)
		df["turnoverratio"] = df["turnoverratio"].apply(Data.formatFloat)
		df["pe"] = df["pe"].apply(Data.formatFloat)
		df = df.rename(columns={"changepercent":"incr", "turnoverratio":"turnover"})

		return df

if __name__ == "__main__":
	
	df = CanslimStrategy().run()
	print df

