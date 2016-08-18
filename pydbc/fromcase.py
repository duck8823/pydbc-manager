# -*- coding: utf-8 -*-
from pydbc.executable import Executable
from pydbc.where import Where


class FromCase(object):
	def __init__(self, manager, entity):
		self._manager = manager
		self._entity = entity
		self._where = Where()

	def where(self, where):
		self._where = where
		return self

	# noinspection PyProtectedMember
	def list(self):
		result = []

		columns = self._entity._fields
		cursor = self._manager._PydbcManager__connection.cursor()
		cursor.execute("SELECT %s FROM %s %s" % (", ".join(columns), self._entity.__name__, self._where))
		rows = cursor.fetchall()

		for row in rows:
			result.append(self._entity(*row))

		return result

	def single_result(self):
		result = self.list()
		if len(result) > 1:
			raise Exception('結果が一意でありません.')
		return result[0]

	def delete(self):
		return Executable(self._manager, "DELETE FROM %s %s" % (self._entity.__name__, self._where))
