from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.userControl import Register

def tirarExcepcion():
	raise Exception("Token invalido")


class TestEndpointAgregarUsuario(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()


	@patch("src.resources.userControl.mongo")
	@patch("src.resources.userControl.conectividad")
	def test_camino_feliz(self, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = {"user":{"id": "3"}}

		JSON = {"type": "passenger",
			"username": "string",
			"password": "string",
			"fb": {
			"userId": "string",
			"authToken": "string"
			},
			"firstName": "string",
			"lastName": "string",
			"country": "string",
			"email": "string",
			"birthdate": "string",
			"image": "string"
			}
		
		rv = self.app.post('users', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertEqual(rv.status_code,201)



