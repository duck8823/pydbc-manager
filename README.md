# PydbcManager
[![Build Status](https://travis-ci.org/duck8823/pydbc-manager.svg?branch=master)](https://travis-ci.org/duck8823/pydbc-manager)
[![Coverage Status](https://coveralls.io/repos/github/duck8823/pydbc-manager/badge.svg?branch=master)](https://coveralls.io/github/duck8823/pydbc-manager?branch=master)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)  
  
名前付きタプルでデータベースを操作する    
  
## INSTALL
```sh
git clone https://github.com/duck8823/pydbc-manager.git
cd pydbc-manager
sudo python setup.py install
```
  
## SYNOPSIS
```python
# -*- coding: utf-8 -*-
import psycopg2 as driver
from pydbc import *

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
```

## License
MIT License
