# -*- coding: utf-8 -*-
from pydbc.fromcase import FromCase
from pydbc.executable import Executable


def connect(driver, datasource):
	return PydbcManager(driver, datasource)


class PydbcManager(object):
	def __init__(self, driver, datasource):
		self.__connection = driver.connect(datasource)

	def frm(self, entity):
		return FromCase(self, entity)

	def drop(self, entity):
		return Executable(self, "DROP TABLE IF EXISTS %s" % entity.__name__)

	def create(self, entity):
		# noinspection PyProtectedMember
		dict_ = entity._asdict()
		columns = []
		for name in dict_:
			type_ = dict_[name]
			if type_ == int:
				type_ = 'INTEGER'
			elif type_ == str:
				type_ = 'TEXT'
			elif type_ == bool:
				type_ = 'BOOLEAN'
			else:
				raise Exception('次の型は利用できません: ' + type_.__name__)
			columns.append("%s %s" % (name, type_))
		return Executable(self, "CREATE TABLE %s (%s)" % (entity.__class__.__name__, ", ".join(columns)))

	def insert(self, data):
		sentence = self._create_sentence(data)
		return Executable(self, "INSERT INTO %s %s" % (data.__class__.__name__, sentence))

	@staticmethod
	def _create_sentence(data):
		# noinspection PyProtectedMember
		dict_ = data._asdict()
		columns = []
		values = []
		for name in dict_:
			value = dict_[name]
			if not isinstance(value, int) and not isinstance(value, str) and not isinstance(value, bool):
				raise Exception("次の型は対応していません. %s (%s)" % (name, value.__class__.__name__))
			columns.append(name)
			values.append("'%s'" % str(value))
		return "(%s) VALUES (%s)" % (", ".join(columns), ", ".join(values))
