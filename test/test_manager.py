# -*- coding: utf-8 -*-
import unittest
import sqlite3 as driver

from pydbc import *
from pydbc.manager import PydbcManager

Test = namedtuple('Test', 'id name flg')
datasource = 'test.db'


class TestPydbcManager(unittest.TestCase):
	def test_connection(self):
		manager = connect(driver, datasource)
		self.assertEqual(manager.__class__, PydbcManager)

	def test_create(self):
		manager = connect(driver, datasource)
		manager.drop(Test).execute()
		manager.create(Test(id=int, name=str, flg=bool)).execute()

		cursor = manager._db.cursor()
		cursor.execute("PRAGMA TABLE_INFO(test)")
		rows = cursor.fetchall()

		actual = {}
		for row in rows:
			actual[row[1]] = row[2]

		self.assertEqual(actual, {'id': 'INTEGER', 'name': 'TEXT', 'flg': 'BOOLEAN'})

	def test_drop(self):
		manager = connect(driver, datasource)
		manager.drop(Test).execute()
		manager.create(Test(id=int, name=str, flg=bool)).execute()

		manager.drop(Test).execute()

		cursor = manager._db.cursor()
		cursor.execute("PRAGMA TABLE_INFO(test)")
		rows = cursor.fetchall()

		self.assertEqual(len(rows), 0, "カラムが存在します.")

	def test_insert(self):
		manager = connect(driver, datasource)
		manager.drop(Test).execute()
		manager.create(Test(id=int, name=str, flg=bool)).execute()

		manager.insert(Test(1, 'name_1', True)).execute()
		manager.insert(Test(2, 'name_2', False)).execute()

		expect = [(1, 'name_1', 'True'), (2, 'name_2', 'False')]
		cursor = manager._db.cursor()
		cursor.execute("SELECT id, name, flg FROM test")
		actual = cursor.fetchall()
		self.assertEqual(actual, expect, 'データが一致しません.')

	def test_create_sentence(self):
		actual = PydbcManager._create_sentence(Test(1, 'name_1', True))
		self.assertEqual(actual, "(id, name, flg) VALUES ('1', 'name_1', 'True')")

		Fail = namedtuple('Fail', 'fail')

		with self.assertRaises(Exception):
			PydbcManager._create_sentence(Fail(fail=bytearray))
