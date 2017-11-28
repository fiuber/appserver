from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.eliminarAutoUsuario import EliminarAutoUsuario

def tirarExcepcion():
	raise Exception("")


class TestEndpointEliminarAutoUsuario(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()


	@patch("src.resources.eliminarAutoUsuario.mongo")
	@patch("src.resources.eliminarAutoUsuario.conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_camino_feliz(self, mockToken, mockConectividad, mockMongo):

		mockMongo.db.conductores.find_and_modify.return_value = {"autoActivo": "8", "autosRegistrados": ["1", "2", "8"]}
		mockMongo.db.conductores.update.return_value = {"nModified": 1}
		mockConectividad.delete.return_value = True
		mockToken.return_value.validarToken.return_value = True
		
		rv = self.app.delete('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,200)

	@patch("src.resources.eliminarAutoUsuario.mongo")
	@patch("src.resources.eliminarAutoUsuario.conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_camino_feliz_sin_autos_al_final(self, mockToken, mockConectividad, mockMongo):

		mockMongo.db.conductores.find_and_modify.return_value = {"autoActivo": "8", "autosRegistrados": []}
		mockMongo.db.conductores.update.return_value = {"nModified": 1}
		mockConectividad.delete.return_value = True
		mockToken.return_value.validarToken.return_value = True
		
		rv = self.app.delete('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,200)

	@patch("src.resources.eliminarAutoUsuario.mongo")
	@patch("src.resources.eliminarAutoUsuario.conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_sin_token(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.delete.return_value = True
		mockToken.return_value.validarToken.return_value = True
		
		rv = self.app.delete('/driver/3/cars/8')

		self.assertEqual(rv.status_code,403)

	@patch("src.resources.eliminarAutoUsuario.mongo")
	@patch("src.resources.eliminarAutoUsuario.conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_token_invalido(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.delete.return_value = True
		mockToken.return_value.validarToken.return_value = False
		
		rv = self.app.delete('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.eliminarAutoUsuario.mongo")
	@patch("src.resources.eliminarAutoUsuario.conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_conexion_fallida(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = True
		mockConectividad.delete.return_value = False
		mockToken.return_value.validarToken.return_value = True

		rv = self.app.delete('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 404)
