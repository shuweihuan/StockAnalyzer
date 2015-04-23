#!/usr/bin/python
#coding: utf-8

import os

class File:

	@staticmethod
	def getFileName(path):
		file_name = os.path.basename(path)
		f = file_name.split(".")
		return f[0]

	@staticmethod
	def getFileDate(path):
		file_name = os.path.basename(path)
		f = file_name.split(".")
		return f[1]

	@staticmethod
	def getFileType(path):
		file_name = os.path.basename(path)
		f = file_name.split(".")
		return f[2]

	@staticmethod
	def getLatestDate(path, name=''):
		latest_date = ""
		for f in os.listdir(path):
			f_name = File.getFileName(f)
			f_date = File.getFileDate(f)
			if name == "":
				if f_date > latest_date:
					latest_date = f_date
			elif f_name == name:
				if f_date > latest_date:
					latest_date = f_date
		return latest_date

	@staticmethod
	def getLatestFile(path, name):
		all_files = os.listdir(path)
		if all_files == []:
			return ""
		files = []
		for f in all_files:
			if File.getFileName(f) == name:
				files.append(f)
		if files == []:
			return ""
		files.sort()
		latest_file = os.path.join(path, files[-1])
		return latest_file

