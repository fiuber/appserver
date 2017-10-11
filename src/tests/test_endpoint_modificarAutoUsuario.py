from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.modificarAutoUsuario import ModificarAutoUsuario

def tirarExcepcion():
	raise Exception("")


class TestEndpointModificarAutoUsuario(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()



	@patch("src.resources.modificarAutoUsuario.Conectividad")
	@patch("src.resources.modificarAutoUsuario.Token")
	def test_camino_feliz(self, mockToken, mockConectividad):

		mockConectividad.return_value.put.return_value = True
		mockToken.return_value.validarToken.return_value = True

		JSON = {"modelo": "2001",
		        "color": "Azul",
			"patente": "ABC-001",
			"anio": "2001",
			"estado": "hecho mierda",
			"aireAcondicionado": "ni en pedo",
			"musica": "cumbia villera"}
		
		rv = self.app.put('/driver/3/cars/8', 
				  data = json.dumps(JSON),
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,200)


	@patch("src.resources.modificarAutoUsuario.Conectividad")
	@patch("src.resources.modificarAutoUsuario.Token")
	def test_sin_token(self, mockToken, mockConectividad):

		mockConectividad.return_value.put.return_value = True
		mockToken.return_value.validarToken.return_value = True

		JSON = {"modelo": "2001",
		        "color": "Azul",
			"patente": "ABC-001",
			"anio": "2001",
			"estado": "hecho mierda",
			"aireAcondicionado": "ni en pedo",
			"musica": "cumbia villera"}
		
		rv = self.app.put('/driver/3/cars/8', 
				  data = json.dumps(JSON),
				  content_type = "application/json")

		self.assertEqual(rv.status_code,403)

	@patch("src.resources.modificarAutoUsuario.Conectividad")
	@patch("src.resources.modificarAutoUsuario.Token")
	def test_sin_json(self, mockToken, mockConectividad):

		mockConectividad.return_value.put.return_value = True
		mockToken.return_value.validarToken.return_value = True

		rv = self.app.put('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,500)

	@patch("src.resources.modificarAutoUsuario.Conectividad")
	@patch("src.resources.modificarAutoUsuario.Token")
	def test_token_invalido(self, mockToken, mockConectividad):

		mockConectividad.return_value.put.return_value = True
		mockToken.return_value.validarToken.return_value = False

		JSON = {"modelo": "2001",
		        "color": "Azul",
			"patente": "ABC-001",
			"anio": "2001",
			"estado": "hecho mierda",
			"aireAcondicionado": "ni en pedo",
			"musica": "cumbia villera"}
		
		rv = self.app.put('/driver/3/cars/8', 
				  data = json.dumps(JSON),
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.modificarAutoUsuario.Conectividad")
	@patch("src.resources.modificarAutoUsuario.Token")
	def test_conexion_fallida(self, mockToken, mockConectividad):

		mockConectividad.return_value.put.return_value = False
		mockToken.return_value.validarToken.return_value = True

		JSON = {"modelo": "2001",
		        "color": "Azul",
			"patente": "ABC-001",
			"anio": "2001",
			"estado": "hecho mierda",
			"aireAcondicionado": "ni en pedo",
			"musica": "cumbia villera"}
		
		rv = self.app.put('/driver/3/cars/8', 
				  data = json.dumps(JSON),
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 404)
