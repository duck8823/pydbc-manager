# -*- coding: utf-8 -*-
import enum


class Operator(enum.Enum):
	EQUAL = '='
	NOT_EQUAL = '<>'
	LIKE = 'LIKE'


class Where(object):
	def __init__(self, column=None, value=None, operator=None):
		self.column = column
		self.value = value
		self.operator = operator

	def __str__(self):
		if self.column is None and self.value is None and self.operator is None:
			return ''
		elif (self.column is not None and self.value is None) or (self.column is None and self.value is not None):
			raise Exception("error: %s" % self.__dict__)
		if not isinstance(self.value, int) and not isinstance(self.value, str) and not isinstance(self.value, bool):
			raise Exception("次の方は対応していません. %s (%s)" % (self.column, self.value.__class__.__name__))
		if self.operator == Operator.LIKE:
			self.value = '%' + str(self.value) + '%'
		return "WHERE %s %s '%s'" % (self.column, self.operator.value, self.value)
