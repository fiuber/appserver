from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.userControl import UserController

def tirarExcepcion():
	raise Exception("")


class TestEndpointEliminarUsuario(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()


	@patch("src.resources.userControl.mongo")
	@patch("src.resources.userControl.conectividad")
	def test_camino_feliz(self, mockConectividad, mockMongo):

		mockMongo = True
		
		mockConectividad.delete.return_value = True
		
		rv = self.app.delete('/users/3',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,204)


