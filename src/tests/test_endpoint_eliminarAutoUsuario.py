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



	@patch("src.resources.eliminarAutoUsuario.Conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_camino_feliz(self, mockToken, mockConectividad):

		mockConectividad.return_value.delete.return_value = True
		mockToken.return_value.validarToken.return_value = True
		
		rv = self.app.delete('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code,200)


	@patch("src.resources.eliminarAutoUsuario.Conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_sin_token(self, mockToken, mockConectividad):

		mockConectividad.return_value.delete.return_value = True
		mockToken.return_value.validarToken.return_value = True
		
		rv = self.app.delete('/driver/3/cars/8')

		self.assertEqual(rv.status_code,403)


	@patch("src.resources.eliminarAutoUsuario.Conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_token_invalido(self, mockToken, mockConectividad):

		mockConectividad.return_value.delete.return_value = True
		mockToken.return_value.validarToken.return_value = False
		
		rv = self.app.delete('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.eliminarAutoUsuario.Conectividad")
	@patch("src.resources.eliminarAutoUsuario.Token")
	def test_conexion_fallida(self, mockToken, mockConectividad):

		mockConectividad.return_value.delete.return_value = False
		mockToken.return_value.validarToken.return_value = True

		rv = self.app.delete('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 404)
