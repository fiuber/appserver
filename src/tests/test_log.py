from mock import patch, MagicMock, PropertyMock
import unittest
import jwt

from src.models.log import Log

class TestLog(unittest.TestCase):

	@patch("src.models.log.mongo")
	def test_logerror(self, mockMongo):
		mockMongo.return_value = True
	
		self.assertTrue(Log.errorLog("Hola"))

	@patch("src.models.log.mongo")
	def test_loginfo(self, mockMongo):
		mockMongo.return_value = True
	
		self.assertTrue(Log.infoLog("Hola"))

	@patch("src.models.log.mongo")
	def test_logwarning(self, mockMongo):
		mockMongo.return_value = True
	
		self.assertTrue(Log.warningLog("Hola"))

	@patch("src.models.log.mongo")
	def test_logcritical(self, mockMongo):
		mockMongo.return_value = True
	
		self.assertTrue(Log.criticalLog("Hola"))	
