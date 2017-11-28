from mock import patch, MagicMock, PropertyMock
import unittest
import jwt

from src.models.push import enviarNotificacionPush


	  


class TestPush(unittest.TestCase):

	@patch("src.models.push.conectividad")
	def test_push(self, mockConectividad):
		mockConectividad.return_value = True
	
		self.assertTrue(enviarNotificacionPush(1,"Hola","Mundo",1))

	
