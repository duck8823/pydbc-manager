import unittest
import sqlite3 as driver

from pydbc import *
from pydbc.manager import PydbcManager


class Test:
	id = int
	name = str
	flg = bool


class TestPydbcManager(unittest.TestCase):
	def test_connection(self):
		manager = connect(driver, "test.db")
		self.assertEqual(manager.__class__, PydbcManager)

	def test_create(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test).execute()

		cursor = manager._PydbcManager__connection.cursor()
		cursor.execute("PRAGMA TABLE_INFO(test)")
		rows = cursor.fetchall()

		actual = {}
		for row in rows:
			actual[row[1]] = row[2]

		self.assertEqual(actual, {'id': 'INTEGER', 'name': 'TEXT', 'flg': 'BOOLEAN'})

	def test_drop(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test).execute()

		manager.drop(Test).execute()

		cursor = manager._PydbcManager__connection.cursor()
		cursor.execute("PRAGMA TABLE_INFO(test)")
		rows = cursor.fetchall()

		self.assertEqual(len(rows), 0, "カラムが存在します.")

	def test_insert(self):
		manager = connect(driver, "test.db")
		manager.drop(Test).execute()
		manager.create(Test).execute()

		manager.insert(_build_test(1, 'name_1', True)).execute()
		manager.insert(_build_test(2, 'name_2', False)).execute()

		expect = [(1, 'name_1', 'True'), (2, 'name_2', 'False')]
		cursor = manager._PydbcManager__connection.cursor()
		cursor.execute("SELECT id, name, flg FROM test")
		actual = cursor.fetchall()
		self.assertEqual(actual, expect, 'データが一致しません.')

	def test_create_sentence(self):
		actual = PydbcManager._create_sentence(_build_test(1, 'name_1', True))
		# 変数名の順番になる
		self.assertEqual(actual, "(flg, id, name) VALUES ('True', '1', 'name_1')")

		class Fail:
			fail_field = bytearray

		fail = Fail()
		with self.assertRaises(Exception):
			PydbcManager._create_sentence(fail)

	def test_readme(self):
		class Hoge:
			dummy = bool

		manager = connect(driver, "test.db")
		manager.drop(Hoge).execute()

		class Hoge:
			id = int
			name = str
			flg = bool

		# データベースへの接続
		manager = connect(driver, "test.db")
		# テーブルの作成
		manager.create(Hoge).execute()
		# データの挿入
		hoge = Hoge()
		hoge.id = 1
		hoge.name = 'name1'
		hoge.flg = True
		manager.insert(hoge).execute()

		hoge = Hoge()
		hoge.id = 2
		hoge.name = 'name2'
		hoge.flg = False
		manager.insert(hoge).execute()
		# データの取得（リスト）
		manager.frm(Hoge).list()
		manager.frm(Hoge).where(Where('name', 'name', Operator.LIKE)).list()
		# データの取得（一意）
		manager.frm(Hoge).where(Where('id', 1, Operator.EQUAL)).single_result()
		# データの削除
		manager.frm(Hoge).where(Where('id', 1, Operator.EQUAL)).delete().execute()
		# テーブルの削除
		manager.drop(Hoge).execute()
		# SQLの取得
		manager.create(Hoge).get_sql()
		hoge = Hoge()
		hoge.id = 1
		hoge.name = 'name1'
		hoge.flg = True
		manager.insert(hoge).get_sql()
		manager.frm(Hoge).where(Where('id', 1, Operator.EQUAL)).delete().get_sql()
		manager.drop(Hoge).get_sql()


def _build_test(id_, name, flg):
	test_ = Test()
	test_.id = id_
	test_.name = name
	test_.flg = flg
	return test_
