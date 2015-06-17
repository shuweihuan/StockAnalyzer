#!/usr/bin/python
#coding: utf-8

import os
import time

class Time:

	@staticmethod
	def today():
		return time.strftime('%Y-%m-%d')

	@staticmethod
	def getPrevQuarter(year, quarter):
		if quarter == 1:
			return year-1, 4
		else:
			return year, quarter-1

	@staticmethod
	def getThisQuarter(today=""):
		if today == "":
			today = Time.today()
		ymd = today.split('-')
		year = int(ymd[0])
		month = int(ymd[1])
		return year, (month+2)/3

	@staticmethod
	def getLastQuarter(today=""):
		y, q = Time.getThisQuarter(today)
		return Time.getPrevQuarter(y, q)

	@staticmethod
	def getFirstDayOfQuarter(year, quarter):
		month = quarter * 3 - 2
		if month < 10:
			return str(year) + '-0' + str(month) + '-01'
		else:
			return str(year) + '-' + str(month) + '-01'

	@staticmethod
	def getLastDayOfQuarter(year, quarter):
		month = quarter * 3
		if quarter == 1 or quarter == 4:
			day = 31
		else:
			day = 30
		if month < 10:
			return str(year) + '-0' + str(month) + '-' + str(day)
		else:
			return str(year) + '-' + str(month) + '-' + str(day)

