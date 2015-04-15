#!/usr/bin/python
#coding: utf-8

class Data:
	
	def __init__(self):
		pass

	def setHead(self, head):
		self.head = head

	def getHead(self):
		return self.head

	def dumpHead(self, fout):
		s = "#"
		for i in self.head:
			s += i
			s += "\t"
		s = s.strip()
		fout.write(s + "\n")
	
	def setBody(self, body):
		self.body = body

	def getBody(self):
		return self.body

	def dumpBody(self, fout):
		for i in self.body:
			s += i
			s += "\t"
		s = strip()
		fout.write(s + "\n")

	def dump(self, fout):
		self.dumpHead(fout)
		self.dumpBody(fout)

