#!/usr/bin/python
#coding: utf-8

import sys

class Data:
	
	def __init__(self, head, body):
		self.head = head
		self.body = body
		self.nCol = len(head)
		self.nRow = len(body)

	def setHead(self, head):
		self.head = head
		self.nCol = len(head)

	def getHead(self):
		return self.head

	def dumpHead(self, fout=sys.stdout):
		s = "\t".join(self.getHead())
		fout.write("#" + s + "\n")
	
	def setBody(self, body):
		self.body = body
		self.nRow = len(body)

	def getBody(self):
		return self.body

	def dumpBody(self, fout=sys.stdout):
		for i in range(self.nRow):
			self.dumpItem(i)

	def dump(self, fout=sys.stdout):
		self.dumpHead(fout)
		self.dumpBody(fout)

	def getItem(self, index):
		return self.body[index]

	def setItem(self, index, item):
		self.body[index] = item

	def dumpItem(self, index, fout=sys.stdout):
		s = "\t".join(self.getItem(index))
		fout.write(s + "\n")

	def catRow(self, data):
		if ( self.getHead() == data.getHead() ):
			r = self.getBody() + data.getBody()
			self.setBody(r)
			return True
		return False

	def catCol(self, data):
		if ( self.nRow == data.nRow ):
			r = self.getHead() + data.getHead()
			self.setHead(r)
			for i in range(self.nRow):
				r = self.getItem(i) + data.getItem(i)
				self.setItem(i, r)
			return True
		return False

if __name__ == "__main__":

	print ""

	a_head = ["A", "B"]
	a_body = [["1","1"],["2","2"],["3","3"]]
	a = Data(a_head, a_body)
	print("* A, %dx%d" % (a.nRow, a.nCol))
	print("---------")
	a.dump()

	print ""

	b_head = ["C"]
	b_body = [["1"],["2"],["3"]]
	b = Data(b_head, b_body)
	print("* B, %dx%d" % (b.nRow, b.nCol))
	print("---------")
	b.dump()

	print ""

	c_head = ["A", "B", "C"]
	c_body = [["4","4","4"]]
	c = Data(c_head, c_body)
	print("* C, %dx%d" % (c.nRow, c.nCol))
	print("---------")
	c.dump()

	print ""

	if ( a.catCol(b) ):
		print("* A.catCol(B), %dx%d" % (a.nRow, a.nCol))
		print("---------")
		a.dump()
	else:
		print "ERROR"

	print ""

	if ( a.catRow(c) ):
		print("* A.catRow(C), %dx%d" % (a.nRow, a.nCol))
		print("---------")
		a.dump()
	else:
		print "ERROR"

