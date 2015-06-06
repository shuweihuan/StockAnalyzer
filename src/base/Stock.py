#!/usr/bin/python
#coding: utf-8

import os
import time
import types

class Stock:

	@staticmethod
	def norm_code(code):
		code = str(code)
		l = 6 - len(code)
		return '0' * l + code

