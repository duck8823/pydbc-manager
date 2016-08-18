# -*- coding: utf-8 -*-
import unittest
import psycopg2 as driver
from pydbc import *


class TestReadme(unittest.TestCase):

	def test_readme(self):

		Hoge = namedtuple('Hoge', 'id name flg')
		manager = connect(driver, 'dbname=test host=localhost user=postgres')
		manager.drop(Hoge).execute()

		# 名前付きタプルの定義
		Hoge = namedtuple('Hoge', 'id name flg')

		# データベースへの接続
		manager = connect(driver, 'dbname=test host=localhost user=postgres')
		# テーブルの作成
		manager.create(Hoge(id=int, name=str, flg=bool)).execute()
		# データの挿入
		manager.insert(Hoge(1, 'name1', True)).execute()
		manager.insert(Hoge(2, 'name2', False)).execute()
		# データの取得（リスト）
		rows = manager.frm(Hoge).list()
		for row in rows:
			print(row)
		manager.frm(Hoge).where(Where('name', 'name', Operator.LIKE)).list()
		# データの取得（一意）
		row = manager.frm(Hoge).where(Where('id', 1, Operator.EQUAL)).single_result()
		print(row)
		# データの削除
		manager.frm(Hoge).where(Where('id', 1, Operator.EQUAL)).delete().execute()
		# テーブルの削除
		manager.drop(Hoge).execute()
		# SQLの取得
		createSQL = manager.create(Hoge(id=int, name=str, flg=bool)).get_sql()
		insertSQL = manager.insert(Hoge(1, 'name1', True)).get_sql()
		deleteSQL = manager.frm(Hoge).where(Where('id', 1, Operator.EQUAL)).delete().get_sql()
		dropSQL = manager.drop(Hoge).get_sql()
