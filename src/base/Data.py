#!/usr/bin/python
#coding: utf-8

import sys

class Data:
	
	def __init__(self, head=[], body=[]):
		self.head = head
		self.body = body
		self.nCol = len(head)
		self.nRow = len(body)

	def setHead(self, head):
		self.head = head
		self.nCol = len(head)
		return True

	def getHead(self):
		return self.head

	def dumpHead(self, fout=sys.stdout):
		s = "\t".join(self.head)
		fout.write("#" + s + "\n")
	
	def setBody(self, body):
		self.body = body
		self.nRow = len(body)
		return True

	def getBody(self):
		return self.body

	def dumpBody(self, fout=sys.stdout):
		for i in range(self.nRow):
			self.dumpItem(i)

	def dump(self, fout=sys.stdout):
		self.dumpHead(fout)
		self.dumpBody(fout)

	def getItem(self, index):
		if index < self.nRow:
			return self.body[index]
		return []

	def setItem(self, index, item):
		if index < self.nRow:
			self.body[index] = item
			return True
		return False

	def dumpItem(self, index, fout=sys.stdout):
		s = "\t".join(self.getItem(index))
		fout.write(s + "\n")

	def getRow(self, index_list):
		data = Data()
		for i in index_list:
			if i >= self.nRow:
				return data
		data.setHead(self.head)
		body = []
		for i in index_list:
			body.append(self.body[i])
		data.setBody(body)
		return data

	def setRow(self, index_list, rows):
		if len(index_list) > self.nRow:
			return False
		if len(index_list) != len(rows):
			return False
		for i in rows:
			if len(i) != self.nCol:
				return False
		for i in range(len(index_list)):
			if index_list[i] >= self.nRow:
				return False
			self.body[index_list[i]] = rows[i]
		return True

	def getCol(self, key_list):
		data = Data()
		index_list = []
		for key in key_list:
			if not key in self.head:
				return data
			index_list.append(self.head.index(key))
		data.setHead(key_list)
		body = []
		for row in self.body:
			r = []
			for i in index_list:
				r.append(row[i])
			body.append(r)
		data.setBody(body)
		return data

	def setCol(self, key_list, cols):
		if len(key_list) > self.nCol:
			return False
		if len(cols) != self.nRow:
			return False
		for i in cols:
			if len(i) != len(key_list):
				return False
		index_list = []
		for key in key_list:
			if not key in self.head:
				return False
			index_list.append(self.head.index(key))
		for i in range(self.nRow):
			for j in range(len(index_list)):
				self.body[i][index_list[j]] = cols[i][j]
		return True

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

	def join(self, data, key):
		if not key in self.getHead():
			return False
		if not key in data.getHead():
			return False


	def innerJoin(self, data, key):
		pass

	def outerJoin(self, data, key):
		pass

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

	print ""

	print ("* A.setCol(['C'], [['2'],['4'],['6'],['8'])")
	a.setCol(['C'], [['2'],['4'],['6'],['8']])
	a.dump()

	print ""

	print ("* A.getCol(['B','C'])")
	a.getCol(['B','C']).dump()

	print ""

	print ("* A.setRow([2,3], [['6','6','6'],['9','9','9']])")
	a.setRow([2,3], [['6','6','6'],['9','9','9']])
	a.dump()

	print ""

	print ("* A.getRow(range(2,4))")
	a.getRow(range(2,4)).dump()

	print ""

