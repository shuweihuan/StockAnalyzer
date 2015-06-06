#!/usr/bin/python
#coding: utf-8

import os
import time

class Time:

	@staticmethod
	def today():
		return time.strftime('%Y-%m-%d')

	@staticmethod
	def getLastQuarter(today=""):
		if today == "":
			today = Time.today()
		ymd = today.split('-')
		year = int(ymd[0])
		month = int(ymd[1])
		day = int(ymd[2])
		if month >= 1 and month <= 3:
			lr_year = year - 1
			lr_quarter = 4
		else:
			lr_year = year
			lr_quarter = (month-1) / 3
		return [lr_year, lr_quarter]

