# -*- coding: utf-8 -*-
import unittest
import sqlite3 as driver

from pydbc import *

Test = namedtuple('Test', 'id name')


class TestFromCase(unittest.TestCase):
	def test_list(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test(id=int, name=str)).execute()

		manager.insert(Test(1, 'name_1')).execute()
		manager.insert(Test(2, 'name_2')).execute()

		actual = manager.frm(Test).list()
		self.assertEqual(len(actual), 2)
		self.assertEqual(actual[0], Test(id=1, name='name_1'))
		self.assertEqual(actual[1], Test(id=2, name='name_2'))

		with self.assertRaises(Exception):
			manager.frm(Test).where(Where('id', bytearray(), Operator.EQUAL)).list()

		class NotExist:
			id = int

		with self.assertRaises(Exception):
			manager.frm(NotExist).list()

	def test_single_result(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test(id=int, name=str)).execute()

		manager.insert(Test(1, 'name_1')).execute()
		manager.insert(Test(2, 'name_2')).execute()

		actual = manager.frm(Test).where(Where('id', 1, Operator.EQUAL)).single_result()
		expect = Test(id=1, name='name_1')
		self.assertEqual(actual, expect)

		with self.assertRaises(Exception):
			manager.frm(Test).where(Where('id', bytearray(), Operator.EQUAL)).list()

		with self.assertRaises(Exception):
			manager.frm(Test).single_result()

	def test_delete(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test(id=int, name=str)).execute()

		manager.insert(Test(1, 'name_1')).execute()
		manager.insert(Test(2, 'name_2')).execute()

		manager.frm(Test).where(Where('id', 1, Operator.EQUAL)).delete().execute()
		actual = manager.frm(Test).single_result()
		expect = Test(id=2, name='name_2')
		self.assertEqual(actual, expect)

