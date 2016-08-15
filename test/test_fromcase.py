# -*- coding: utf-8 -*-
import unittest
import sqlite3 as driver

from pydbc import connect, Where, Operator


class Test:
	id = int
	name = str
	flg = bool


class TestFromCase(unittest.TestCase):
	def test_list(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test).execute()

		manager.insert(_build_test(1, 'name_1', True)).execute()
		manager.insert(_build_test(2, 'name_2', False)).execute()

		actual = manager.frm(Test).list()
		self.assertEquals(len(actual), 2)
		self.assertDictEqual(actual[0].__dict__, {'id': 1, 'name': 'name_1', 'flg': True})
		self.assertDictEqual(actual[1].__dict__, {'id': 2, 'name': 'name_2', 'flg': False})

		with self.assertRaises(Exception):
			manager.frm(Test).where(Where('id', bytearray(), Operator.EQUAL)).list()

		class NotExist:
			id = int

		with self.assertRaises(Exception):
			manager.frm(NotExist).list()

	def test_single_result(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test).execute()

		manager.insert(_build_test(1, 'name_1', True)).execute()
		manager.insert(_build_test(2, 'name_2', False)).execute()

		actual = manager.frm(Test).where(Where('id', 1, Operator.EQUAL)).single_result()
		expect = {'id': 1, 'name': 'name_1', 'flg': True}
		self.assertDictEqual(actual.__dict__, expect)

		with self.assertRaises(Exception):
			manager.frm(Test).where(Where('id', bytearray(), Operator.EQUAL)).list()

		with self.assertRaises(Exception):
			manager.frm(Test).single_result()

	def test_delete(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test).execute()

		manager.insert(_build_test(1, 'name_1', True)).execute()
		manager.insert(_build_test(2, 'name_2', False)).execute()

		manager.frm(Test).where(Where('id', 1, Operator.EQUAL)).delete().execute()
		actual = manager.frm(Test).single_result()
		expect = {'id': 2, 'name': 'name_2', 'flg': False}
		self.assertDictEqual(actual.__dict__, expect)


def _build_test(id_, name, flg):
	test_ = Test()
	test_.id = id_
	test_.name = name
	test_.flg = flg
	return test_
