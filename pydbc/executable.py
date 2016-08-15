class Executable(object):
	def __init__(self, manager, sql):
		self._manager = manager
		self._sql = sql

	def execute(self):
		# noinspection PyProtectedMember
		cursor = self._manager._PydbcManager__connection
		cursor.execute(self._sql)
		cursor.commit()

	def get_sql(self):
		return self._sql
