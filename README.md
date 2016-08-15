# GodbcManager
[![Build Status](https://travis-ci.org/duck8823/pydbc-manager.svg?branch=master)](https://travis-ci.org/duck8823/pydbc-manager)
[![Coverage Status](http://coveralls.io/repos/github/duck8823/pydbc-manager/badge.svg?branch=master)](https://coveralls.io/github/duck8823/pydbc-manager?branch=master)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)  
  
構造体でデータベース操作する  
  
## INSTALL
```sh
git clone https://github.com/duck8823/pydbc-manager.git
cd pydbc-manager
python setup.py install
```
  
## SYNOPSIS
```python
from pydbc import *


# クラスの定義
class Hoge:
	id = int
	name = str
	flg = bool


def main:
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
```

## License
MIT License