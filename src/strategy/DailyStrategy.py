#!/usr/bin/python
#coding: utf-8

import os
import sys
import pandas as pd
from Strategy import Strategy
sys.path.append("..")
from base.Time import Time
from base.Singleton import Singleton

class DailyStrategy(Strategy):

	def run(self, time="", save=False, load=False):
		df = pd.DataFrame()
		if time == "":
			time = Time.today()
		if load:
			df = self._load(time)
		if df.empty:
			df = self.calc(time)
		if save:
			self._save(df, time)
		return df

	def test(self):
		pass

