# -*- coding: utf-8 -*-
class Executable(object):
	def __init__(self, manager, sql):
		self._manager = manager
		self._sql = sql

	# noinspection PyProtectedMember
	def execute(self):
		cursor = self._manager._PydbcManager__connection.cursor()
		cursor.execute(self._sql)
		self._manager._PydbcManager__connection.commit()

	def get_sql(self):
		return self._sql
