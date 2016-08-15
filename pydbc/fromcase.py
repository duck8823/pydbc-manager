from pydbc.executable import Executable
from pydbc.where import Where
import ast
import re
import inspect


class FromCase(object):
	def __init__(self, manager, entity):
		self._manager = manager
		self._entity = entity
		self._where = Where()

	def where(self, where):
		self._where = where
		return self

	def list(self):
		result = []

		attrs = filter(lambda a: not re.match("^__.*__$", a[0]), inspect.getmembers(self._entity))
		columns = []
		for attr in attrs:
			columns.append(attr[0])

		# noinspection PyProtectedMember
		cursor = self._manager._PydbcManager__connection.cursor()
		cursor.execute("SELECT %s FROM %s %s" % (", ".join(columns), self._entity.__name__, self._where))
		rows = cursor.fetchall()

		for row in rows:
			entity = self._entity()
			for column in columns:
				value = row[columns.index(column)]
				if self._entity.__dict__[column] == bool:
					value = ast.literal_eval(value)

				setattr(entity, column, value)
			result.append(entity)

		return result

	def single_result(self):
		result = self.list()
		if len(result) > 1:
			raise Exception('結果が一意でありません.')
		return result[0]

	def delete(self):
		return Executable(self._manager, "DELETE FROM %s %s" % (self._entity.__name__, self._where))
