#!/usr/bin/python
#coding: utf-8

import os

class File:

	@staticmethod
	def getLatestFileName(path, n=1):
		if not os.path.isdir(path):
			return ""
		all_files = os.listdir(path)
		if len(all_files) < n:
			return ""
		all_files.sort()
		return all_files[0-n]

	@staticmethod
	def getLatestFilePath(path, n=1):
		file_name = File.getLatestFileName(path, n)
		return os.path.join(path, file_name)

