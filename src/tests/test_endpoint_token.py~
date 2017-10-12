from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.auth import Auth

def tirarExcepcion():
	raise Exception("Token invalido")


class TestEndpointToken(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()



	@patch("src.resources.auth.Conectividad")
	@patch("src.resources.auth.Token")
	def test_camino_feliz(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = True
		mockToken.return_value.obtenerToken.return_value = "jhefwjdsfkdsf"

		JSON = {"nombreUsuario": "Marcos", "contrasena": "tool"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertEqual(rv.status_code,200)

	@patch("src.resources.auth.Conectividad")
	@patch("src.resources.auth.Token")
	def test_sin_json(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = True
		mockToken.return_value.obtenerToken.return_value = "jhefwjdsfkdsf"

		JSON = {"nombreUsuario": "Marcos", "contrasena": "tool"}
		
		rv = self.app.post('/token')

		self.assertEqual(rv.status_code, 500)


	@patch("src.resources.auth.Conectividad")
	@patch("src.resources.auth.Token")
	def test_fallo_token(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = True
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"nombreUsuario": "Marcos", "contrasena": "tool"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code,200)

	@patch("src.resources.auth.Conectividad")
	@patch("src.resources.auth.Token")
	def test_no_existe_usuario(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = False
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"nombreUsuario": "Marcos", "contrasena": "tool"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code,200)

	@patch("src.resources.auth.Conectividad")
	@patch("src.resources.auth.Token")
	def test_no_se_manda_usuario(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = False
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"contrasena": "tool"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code,200)

	@patch("src.resources.auth.Conectividad")
	@patch("src.resources.auth.Token")
	def test_no_se_manda_contrasena(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = False
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"nombreUsuario": "Marcos"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code, 200)
