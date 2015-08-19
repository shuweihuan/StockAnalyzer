#!/usr/bin/python
#coding: utf-8

################
# Super Volume #
################

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
from base.File import File
from base.Data import Data
from base.Stock import Stock
from analyzer.analyze_stock_data import *

class SuperVolumeStrategy(DailyStrategy):

	def calc(self, time):
	
		df = Stock.get_stock_info().reset_index()
		df = df.drop("volume", axis=1)
		trading_df = get_stock_trading_features(time).reset_index()
		df = pd.merge(df, trading_df, on="code", how="outer")
		df = df.set_index("code")
		df["v/v_ma5"] = df["volume"] / df["volume_ma5"]
	
		# 当日价格上涨，且日成交量远大于5日均量
		df = df[ ( df["close_incr"] > 0 ) & ( df["v/v_ma5"] > 1.6 ) ]
	
		# 格式优化
		df = df[["name", "close_incr", "v/v_ma5", "turnoverratio", "pe", "industry", "concept" ]]
		df = df.sort_index(by="v/v_ma5", ascending=False)
		df["close_incr"] = df["close_incr"].apply(Data.formatPercentage)
		df["v/v_ma5"] = df["v/v_ma5"].apply(Data.formatFloat)
		df["turnoverratio"] = df["turnoverratio"].apply(Data.formatFloat)
		df["pe"] = df["pe"].apply(Data.formatFloat)
		df = df.rename(columns={"close_incr":"incr", "turnoverratio":"turnover"})
	
		return df
		
if __name__ == "__main__":
	
	df = SuperVolumeStrategy().run()
	print df

