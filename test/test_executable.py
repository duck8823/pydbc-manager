import unittest
import sqlite3 as driver

from pydbc import connect


class TestExecutable(unittest.TestCase):
	def test_execute(self):
		manager = connect(driver, "test.db")

		class Fail:
			id = int
			fail = bytearray

		with self.assertRaises(Exception):
			manager.create(Fail).execute()

		class Success:
			id = int
			name = str

		manager.drop(Success).execute()
		manager.create(Success).execute()

		with self.assertRaises(Exception):
			manager.create(Success).execute()

	def test_get_sql(self):
		manager = connect(driver, "test.db")

		class Hoge:
			id = int
			name = str

		actual = manager.create(Hoge).get_sql()
		expect = "CREATE TABLE Hoge ('id' INTEGER, 'name' TEXT)"
		self.assertEquals(actual, expect)
