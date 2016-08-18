# -*- coding: utf-8 -*-
import unittest
import sqlite3 as driver

from pydbc import *

datasource = 'test.db'


class TestExecutable(unittest.TestCase):

	def test_execute(self):
		manager = connect(driver, datasource)

		Fail = namedtuple('Fail', 'id fail')

		with self.assertRaises(Exception):
			manager.create(Fail(id=int, fail=bytearray)).execute()

		Success = namedtuple('Success', 'id name')

		manager.drop(Success).execute()
		manager.create(Success(id=int, name=str)).execute()

		with self.assertRaises(Exception):
			manager.create(Success(id=int, name=str)).execute()

	def test_get_sql(self):
		manager = connect(driver, datasource)

		Hoge = namedtuple('Hoge', 'id name')

		actual = manager.create(Hoge(id=int, name=str)).get_sql()
		expect = "CREATE TABLE Hoge (id INTEGER, name TEXT)"
		self.assertEquals(actual, expect)
