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
		self.usuarioDriver = {
				    "user": {
					"id": "2",
					"_ref": "598.763515576072",
					"applicationOwner": "3",
					"type": "driver",
					"cars": [
					    {
						"id": "1",
						"_ref": "344.6639930173605",
						"owner": "2",
						"properties": [
						    {
							"name": "modelo",
							"value": "Gol"
						    },
						    {
							"name": "color",
							"value": "Negro"
						    },
						    {
							"name": "imagen",
							"value": "null"
						    },
						    {
							"name": "aireAcondicionado",
							"value": "No"
						    },
						    {
							"name": "musica",
							"value": "Radio"
						    },
						    {
							"name": "anio",
							"value": "2010"
						    },
						    {
							"name": "estado",
							"value": "Bueno"
						    },
						    {
							"name": "patente",
							"value": "OKS451"
						    }
						]
					    }
					],
					"username": "choferFranco",
					"name": "Franco",
					"surname": "Etcheverri",
					"country": "Argentina",
					"email": "franco@fiuber.com",
					"birthdate": "19/6/1994",
					"balance": [],
					"images": [
					    "1.png",
					    "2.png",
					    "3.png"
					]
				    },
				    "metadata": {
					"version": "1"
				    }
				}
		src.server.app.testing = True
		self.app = src.server.app.test_client()


	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_camino_feliz(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = self.usuarioDriver
		mockToken.return_value.obtenerToken.return_value = "jhefwjdsfkdsf"

		JSON = {"nombreUsuario": "Marcos", "contrasena": "tool"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertEqual(rv.status_code,200)

	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_sin_json(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = self.usuarioDriver
		mockToken.return_value.obtenerToken.return_value = "jhefwjdsfkdsf"

		JSON = {"nombreUsuario": "Marcos", "contrasena": "tool"}
		
		rv = self.app.post('/token')

		self.assertEqual(rv.status_code, 500)

	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_fallo_token(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = self.usuarioDriver
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"nombreUsuario": "Marcos", "contrasena": "tool"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code,200)

	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_no_existe_usuario(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = False
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"nombreUsuario": "Marcos", "contrasena": "tool"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code, 200)

	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_no_se_manda_usuario(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = False
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"contrasena": "tool"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code,200)


	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_no_se_manda_contrasena(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = False
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"nombreUsuario": "Marcos"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code, 200)





	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_camino_feliz_facebook(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = self.usuarioDriver
		mockConectividad.get.return_value = {"id": "1231654"}
		mockToken.return_value.obtenerToken.return_value = "jhefwjdsfkdsf"

		JSON = {"tokenFacebook": "123456789"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertEqual(rv.status_code,200)

	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_sin_json_facebook(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = self.usuarioDriver
		mockToken.return_value.obtenerToken.return_value = "jhefwjdsfkdsf"

		JSON = {"tokenFacebook": "123456789"}
		
		rv = self.app.post('/token')

		self.assertEqual(rv.status_code, 500)

	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_fallo_token_facebook(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = self.usuarioDriver
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"tokenFacebook": "123456789"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code,200)

	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_no_existe_usuario_facebook(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = self.usuarioDriver
		mockConectividad.get.return_value = False
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {"tokenFacebook": "123456789"}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code, 200)

	@patch("src.resources.auth.mongo")
	@patch("src.resources.auth.conectividad")
	@patch("src.resources.auth.Token")
	def test_no_se_manda_token_facebook(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.post.return_value = False
		mockToken.return_value.obtenerToken.return_value = False

		JSON = {}
		
		rv = self.app.post('/token', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertNotEqual(rv.status_code,200)


