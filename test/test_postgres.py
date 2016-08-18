# -*- coding: utf-8 -*-
import unittest
import psycopg2 as driver
from pydbc import *

datasource = 'dbname=test host=localhost user=postgres'


class TestPostgres(unittest.TestCase):

	def test_postgres(self):
		manager = connect(driver, datasource)

		Hoge = namedtuple('Hoge', 'id name flg')
		manager.drop(Hoge).execute()
		manager.create(Hoge(id=int, name=str, flg=bool)).execute()

		manager.insert(Hoge(1, 'name_1', True)).execute()
		manager.insert(Hoge(2, 'name_2', False)).execute()

		actual = manager.frm(Hoge).list()
		expect = [Hoge(1, 'name_1', True), Hoge(2, 'name_2', False)]
		self.assertListEqual(actual, expect)

		manager.drop(Hoge).execute()



