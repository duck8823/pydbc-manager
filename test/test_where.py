# -*- coding: utf-8 -*-
import unittest

from pydbc import Operator, Where


class TestWhere(unittest.TestCase):
	def test_new(self):
		where = Where()
		self.assertEqual(where.__class__, Where)

	def test_tostring(self):
		where = Where(None, 1, Operator.EQUAL)
		with self.assertRaises(Exception):
			str(where)

		where = Where('id', None, Operator.EQUAL)
		with self.assertRaises(Exception):
			str(where)

		where = Where(None, None, Operator.EQUAL)
		with self.assertRaises(Exception):
			str(where)

		where = Where('id', bytearray(), Operator.EQUAL)
		with self.assertRaises(Exception):
			str(where)

		expect = "WHERE name LIKE '%name%'"
		actual = str(Where('name', 'name', Operator.LIKE))
		self.assertEqual(actual, expect)

	def test_operator(self):
		self.assertEqual(Operator.EQUAL.value, '=')
		self.assertEqual(Operator.NOT_EQUAL.value, '<>')
		self.assertEqual(Operator.LIKE.value, 'LIKE')
