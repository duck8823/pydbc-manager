# -*- coding: utf-8 -*-
class Executable(object):
	def __init__(self, db, sql):
		self._db = db
		self._sql = sql

	# noinspection PyProtectedMember
	def execute(self):
		cursor = self._db.cursor()
		cursor.execute(self._sql)
		self._db.commit()

	def get_sql(self):
		return self._sql
