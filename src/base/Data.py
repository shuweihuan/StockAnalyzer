#!/usr/bin/python
#coding: utf-8

import sys

class Data:
	
	def __init__(self, head=[], body=[]):
		self.head = head
		self.body = body
		self.nCol = len(head)
		self.nRow = len(body)
		for r in body:
			assert len(r) == self.nCol

	def dumpHead(self, fout=sys.stdout):
		s = "\t".join(self.head)
		fout.write("#" + s + "\n")
	
	def dumpBody(self, fout=sys.stdout):
		for i in range(self.nRow):
			self.dumpItem(i, fout)

	def dump(self, fout=sys.stdout):
		self.dumpHead(fout)
		self.dumpBody(fout)

	def getItem(self, index):
		if index < self.nRow:
			return self.body[index]
		return []

	def addItem(self, item):
		if len(item) == self.nCol:
			self.body.append(item)
			self.nRow += 1
			return True
		return False

	def setItem(self, index, item):
		if index < self.nRow:
			self.body[index] = item
			return True
		return False

	def dumpItem(self, index, fout=sys.stdout):
		s = "\t".join(self.getItem(index))
		fout.write(s + "\n")

	def getAttr(self, key):
		attr = []
		index = self.head.index(key)
		if index < 0:
			return []
		for r in self.body:
			attr.append([r[index]])
		return attr
	
	def getReversedAttr(self, key):
		attr = []
		index = self.head.index(key)
		if index < 0:
			return []
		for r in self.body:
			attr.append(r[index])
		return attr

	def addAttr(self, key, value):
		if key in self.head:
			return False
		if len(value) != self.nRow:
			return False
		self.head.append(key)
		for i in range(self.nRow):
			self.body[i] += value[index]
		self.nCol += 1
		return True

	def dropAttr(self, key):
		index = self.head.index(key)
		if index < 0:
			return False
		del self.head[index]
		for i in range(self.nRow):
			del self.body[i][index]
		self.nCol -= 1
		return True

	def setAttr(self, key, value):
		if len(value) != self.nRow:
			return False
		index = self.head.index(key)
		if index < 0:
			return False
		for i in range(self.nRow):
			self.body[i][index] = value[index][0]
		return True
	
	def dumpAttr(self, key, fout=sys.stdout):
		s = "\n".join(self.getReversedAttr(key))
		fout.write(s + "\n")

	def replaceValue(self, value, new_value):
		n = 0
		for i in range(self.nRow):
			for j in range(self.nCol):
				if self.body[i][j] == value:
					self.body[i][j] = new_value
					n += 1
		return n

	def sortByAttr(self, key, value_type = 'string', reverse = False):
		if not value_type in ['string', 'number']:
			return False
		index = self.head.index(key)
		if index < 0:
			return False
		d = {}
		for r in self.body:
			k = r[index]
			v = r
			d[k] = v
		if value_type == 'string':
			if reverse == False:
				x = sorted(d.items(), lambda x, y: cmp(str(x[0]), str(y[0])))
			else:
				x = sorted(d.items(), lambda x, y: cmp(str(y[0]), str(x[0])))
		if value_type == 'number':
			if reverse == False:
				x = sorted(d.items(), lambda x, y: cmp(float(x[0]), float(y[0])))
			else:
				x = sorted(d.items(), lambda x, y: cmp(float(y[0]), float(x[0])))
		self.body = []
		for k,v in x:
			self.body.append(v)
		return True

	def cat(self, data):
		if self.head == []:
			self.head = data.head
		if self.head != data.head:
			return False
		for r in data.body:
			self.body.append(r)
			self.nRow += 1
		return True

	def load(self, file_path):
		fin = open(file_path, 'r')
		n = 0
		self.head = []
		self.body = []
		for line in fin:
			line = line.strip()
			if n == 0:
				if not line.startswith('#'):
					return False
				self.head = line[1:].split('\t')
			else:
				self.body.append(line.split('\t'))
			n += 1
		self.nCol = len(self.head)
		self.nRow = len(self.body)
		for r in self.body:
			assert len(r) == self.nCol
		fin.close()
		return True

	def innerJoin(self, data, key_a, key_b):
		return self._join(data, key_a, key_b, 'inner')

	def outerJoin(self, data, key_a, key_b, default_value='-'):
		return self._join(data, key_a, key_b, 'outer', default_value)

	def leftJoin(self, data, key_a, key_b, default_value='-'):
		return self._join(data, key_a, key_b, 'left', default_value)

	def _join(self, data, key_a, key_b, join_type, default_value='-'):
		if not join_type in ['inner', 'outer', 'left']:
			return []
		key_a_index = self.head.index(key_a)
		key_b_index = data.head.index(key_b)
		if key_a_index < 0 or key_b_index < 0:
			return []
		head = self.head + data.head[0:key_b_index] + data.head[key_b_index+1:]
		dict_a = {}
		for r in self.body:
			attr_a = r[key_a_index]
			dict_a[attr_a] = r
		dict_b = {}
		for r in data.body:
			attr_b = r[key_b_index]
			dict_b[attr_b] = r[0:key_b_index] + r[key_b_index+1:]
		body = []
		if join_type == "inner":
			attr_set = set(self.getReversedAttr(key_a)) & set(data.getReversedAttr(key_b))
			for key in attr_set:
				r = dict_a[key] + dict_b[key]
				body.append(r)
		if join_type == "outer":
			attr_set = set(self.getReversedAttr(key_a)) | set(data.getReversedAttr(key_b))
			for key in attr_set:
				if not key in dict_b:
					r = dict_a[key] + [default_value] * (data.nCol-1)
				elif not key in dict_a:
					r = [default_value] * self.nCol + dict_b[key]
					r[key_a_index] = key
				else:
					r = dict_a[key] + dict_b[key]
				body.append(r)
		if join_type == "left":
			attr_set = set(self.getReversedAttr(key_a))
			for key in attr_set:
				if key in dict_b:
					r = dict_a[key] + dict_b[key]
				else:
					r = dict_a[key] + [default_value] * (data.nCol-1)
				body.append(r)
		return Data(head, body)
				
if __name__ == "__main__":

	print ""

	a_head = ['A', 'B']
	a_body = [['1','1'],['2','2'],['3','3']]
	a = Data(a_head, a_body)
	print("* A, %dx%d" % (a.nRow, a.nCol))
	print("---------")
	a.dump()

	print ""

	b_head = ['C']
	b_body = [['1'],['2'],['3']]
	b = Data(b_head, b_body)
	print("* B, %dx%d" % (b.nRow, b.nCol))
	print("---------")
	b.dump()

	print ""

	c_head = ['A', 'B']
	c_body = [['4','4']]
	c = Data(c_head, c_body)
	print("* C, %dx%d" % (c.nRow, c.nCol))
	print("---------")
	c.dump()

	print ""

	print ("* A.getAttr('A')")
	a.dumpAttr('A')

	print ""

	print ("* A.getItem(1)")
	a.dumpItem(1)

	print ""

	d_head = ['A', 'D']
	d_body = [['2','4'],['3','6'],['4','8']]
	d = Data(d_head, d_body)
	print("* D, %dx%d" % (d.nRow, d.nCol))
	print("---------")
	d.dump()
	
	print ""

	print ("* A.innerJoin(D, 'A', 'A')")
	a.innerJoin(d,'A','A').dump()

	print ""

	print ("* A.innerJoin(D, 'A', 'A'); A.sortByAttr('A')")
	x = a.innerJoin(d,'A','A')
	x.sortByAttr('A')
	x.dump()

	print ""

	print ("* A.outerJoin(D, 'A', 'A', 'n/a')")
	a.outerJoin(d,'A','A','n/a').dump()

	print ""

	print ("* A.outerJoin(D, 'A', 'A', 'n/a'); A.replaceValue('n/a', '-')")
	x = a.outerJoin(d,'A','A','n/a')
	x.replaceValue('n/a', '-')
	x.dump()

	print ""

	print ("* A.leftJoin(D, 'A', 'A')")
	a.leftJoin(d,'A','A').dump()

	print ""

