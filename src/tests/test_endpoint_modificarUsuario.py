from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.userControl import UserController

def tirarExcepcion():
	raise Exception("")


class TestEndpointModificarUsuario(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()


	@patch("src.resources.userControl.mongo")
	@patch("src.resources.userControl.conectividad")
	def test_camino_feliz(self, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.get.return_value = { "user": {"_ref": "108.168",
						     "name": "retr",
						     "surname": "fdsfdsdfdf",
						     "email": "reetr",
						     "birthdate": "fdgfdggd",
						     "cars": [{},{},{}],
						     "country": "Alabama",
						     "username": "grggd"}}

		mockConectividad.put.return_value = {"user": {"type": "passenger"}}


		JSON = {"type": "driver",
			"username": "fofofo",
			"password": "fdsfdsfddsfsd",	
			"firstName": "retr",			
		        "lastName": "fdsfdsdfdf",
		        "email": "reetr",
		        "birthdate": "fdgfdggd",
		        "country": "Alabama",
		        "image": "http://www.google.com.ar"}
		
		rv = self.app.put('users/1', 
				  data = json.dumps(JSON),
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,200)

