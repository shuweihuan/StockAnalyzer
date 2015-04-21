#!/usr/bin/python
#coding: utf-8

import sys
import time

class Log:

	@staticmethod
	def notice(msg):
		s = "notice: "
		s += Log._datetime()
		s += " "
		s += msg
		sys.stdout.write(s + "\n")

	@staticmethod
	def warning(msg):
		s = "warning: "
		s += Log._datetime()
		s += " "
		s += msg
		sys.stderr.write(s + "\n")

	@staticmethod
	def error(msg):
		s = "error: "
		s += Log._datetime()
		s += " "
		s += msg
		sys.stderr.write(s + "\n")

	@staticmethod
	def _date():
		return time.strftime('%Y-%m-%d',time.localtime(time.time()))
	
	@staticmethod
	def _time():
		return time.strftime('H:%M:%S',time.localtime(time.time()))

	@staticmethod
	def _datetime():
		return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

if __name__ == "__main__":
		
	Log.warning("test warning")

	Log.error("test error")

