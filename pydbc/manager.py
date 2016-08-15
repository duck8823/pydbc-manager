from pydbc.fromcase import FromCase
from pydbc.executable import Executable
import re
import inspect


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
		attrs = filter(lambda a: not re.match("^__.*__$", a[0]), inspect.getmembers(entity))
		columns = []
		for attr in attrs:
			type_ = attr[1]
			if type_ == int:
				type_ = 'INTEGER'
			elif type_ == str:
				type_ = 'TEXT'
			elif type_ == bool:
				type_ = 'BOOLEAN'
			else:
				raise Exception('次の型は利用できません: ' + type_.__name__)
			columns.append("'%s' %s" % (attr[0], type_))
		return Executable(self, "CREATE TABLE %s (%s)" % (entity.__name__, ", ".join(columns)))

	def insert(self, data):
		sentence = self._create_sentence(data)
		return Executable(self, "INSERT INTO %s %s" % (data.__class__.__name__, sentence))

	@staticmethod
	def _create_sentence(data):
		attrs = filter(lambda a: not re.match("^__.*__$", a[0]), inspect.getmembers(data))
		columns = []
		values = []
		for attr in attrs:
			if not isinstance(attr[1], int) and not isinstance(attr[1], str) and not isinstance(attr[1], bool):
				raise Exception("次の方は対応していません. %s (%s)" % (attr[0], attr[1].__class__.__name__))
			columns.append(attr[0])
			values.append("'%s'" % str(attr[1]))
		return "(%s) VALUES (%s)" % (", ".join(columns), ", ".join(values))

