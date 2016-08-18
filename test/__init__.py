# -*- coding: utf-8 -*-
import unittest

from test.test_manager import TestPydbcManager
from test.test_where import TestWhere
from test.test_fromcase import TestFromCase
from test.test_executable import TestExecutable
from test.test_postgres import TestPostgres
from test.test_readme import TestReadme


def suite():
	suite_ = unittest.TestSuite()
	suites = []
	for class_ in [TestPydbcManager, TestFromCase, TestExecutable, TestWhere, TestPostgres, TestReadme]:
		suites.append(unittest.makeSuite(class_))
	suite_.addTests(suites)
	return suite_
