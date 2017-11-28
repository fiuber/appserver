from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.agregarAutoUsuario import AgregarAutoUsuario

def tirarExcepcion():
	raise Exception("Token invalido")


class TestEndpointAgregarAutoUsuario(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()


	@patch("src.resources.agregarAutoUsuario.mongo")
	@patch("src.resources.agregarAutoUsuario.conectividad")
	@patch("src.resources.agregarAutoUsuario.Token")
	def test_camino_feliz(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.return_value.post.return_value = True
		mockToken.return_value.validarToken.return_value = True

		JSON = {"modelo": "2001",
		        "color": "Azul",
			"patente": "ABC-001",
			"anio": "2001",
			"estado": "hecho mierda",
			"aireAcondicionado": "ni en pedo",
			"musica": "cumbia villera"}
		
		rv = self.app.post('/driver/3/cars', 
				  data = json.dumps(JSON),
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,200)


	@patch("src.resources.agregarAutoUsuario.conectividad")
	@patch("src.resources.agregarAutoUsuario.Token")
	def test_sin_token(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = True
		mockToken.return_value.validarToken.return_value = True

		JSON = {"modelo": "2001",
		        "color": "Azul",
			"patente": "ABC-001",
			"anio": "2001",
			"estado": "hecho mierda",
			"aireAcondicionado": "ni en pedo",
			"musica": "cumbia villera"}
		
		rv = self.app.post('/driver/3/cars', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertEqual(rv.status_code,403)

	@patch("src.resources.agregarAutoUsuario.conectividad")
	@patch("src.resources.agregarAutoUsuario.Token")
	def test_sin_json(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = True
		mockToken.return_value.validarToken.return_value = True

		rv = self.app.post('/driver/3/cars',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,500)

	@patch("src.resources.agregarAutoUsuario.conectividad")
	@patch("src.resources.agregarAutoUsuario.Token")
	def test_token_invalido(self, mockToken, mockConectividad):

		mockConectividad.return_value.post.return_value = True
		mockToken.return_value.validarToken.return_value = False

		JSON = {"modelo": "2001",
		        "color": "Azul",
			"patente": "ABC-001",
			"anio": "2001",
			"estado": "hecho mierda",
			"aireAcondicionado": "ni en pedo",
			"musica": "cumbia villera"}
		
		rv = self.app.post('/driver/3/cars', 
				  data = json.dumps(JSON),
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.agregarAutoUsuario.conectividad")
	@patch("src.resources.agregarAutoUsuario.Token")
	def test_conexion_fallida(self, mockToken, mockConectividad):

		mockConectividad.post.return_value = False
		mockToken.return_value.validarToken.return_value = True

		JSON = {"modelo": "2001",
		        "color": "Azul",
			"patente": "ABC-001",
			"anio": "2001",
			"estado": "hecho mierda",
			"aireAcondicionado": "ni en pedo",
			"musica": "cumbia villera"}
		
		rv = self.app.post('/driver/3/cars', 
				  data = json.dumps(JSON),
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 404)
