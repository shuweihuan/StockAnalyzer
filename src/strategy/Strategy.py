#!/usr/bin/python
#coding: utf-8

import os
import sys
import pandas as pd
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.Time import Time
from base.Singleton import Singleton

class Strategy(Singleton):

	def calc(self, time):
		pass

	def run(self, time, save=False, load=False):
		pass

	def test(self):
		pass

	def getName(self):
		return self.__class__.__name__

	def _save(self, df, time):
		if df.empty:
			return False
		dir_path = os.path.join(STRATEGY_PATH, self.getName())
		if not os.path.isdir(dir_path):
			os.mkdir(dir_path)
		file_path = os.path.join(dir_path, time + ".csv")
		df.to_csv(file_path)
		return True
	
	def _load(self, time):
		dir_path = os.path.join(STRATEGY_PATH, self.getName())
		if not os.path.isdir(dir_path):
			return pd.DataFrame()
		file_path = os.path.join(dir_path, time + ".csv")
		if not os.path.isfile(file_path):
			return pd.DataFrame()
		df = pd.read_csv(file_path, dtype={"code":"object"})
		return df

