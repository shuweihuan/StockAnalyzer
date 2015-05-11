#!/usr/bin/python
#coding: utf-8

import sys
import urllib2

class Spider:

	@staticmethod
	def openUrl(url, t=1000):
		request = urllib2.Request(url)
		request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0')
		opener = urllib2.build_opener()
		return opener.open(request, timeout=t)
	
	@staticmethod
	def getHtml(url):
		request = urllib2.Request(url)
		request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0')
		opener = urllib2.build_opener()
		html = opener.open(request).read()
		return html

