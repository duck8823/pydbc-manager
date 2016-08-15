import unittest

from pydbc.manager import *
from test.test_pydbc import TestPydbcManager
from test.test_where import TestWhere
from test.test_fromcase import TestFromCase
from test.test_executable import TestExecutable


def suite():
	suite_ = unittest.TestSuite()
	suites = []
	for class_ in [TestPydbcManager, TestFromCase, TestExecutable, TestWhere]:
		suites.append(unittest.makeSuite(class_))
	suite_.addTests(suites)
	return suite_
