from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.usuarioModificarPosicion import UsuarioModificarPosicion

def tirarExcepcion():
	raise Exception("")


class TestEndpointUsuarioModificarPosicion(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()

	@patch("src.resources.usuarioModificarPosicion.mongo")
	@patch("src.resources.usuarioModificarPosicion.Token")
	def test_camino_feliz(self, mockToken, mockMongo):

		JSON = {
				"posicion":
				{
				"lat": 42.460387,
				"lng": -71.3489306
				}
			}


		mockToken.return_value.validarToken.return_value = True
		mockMongo.db.usuarios.update.return_value = True
		
		rv = self.app.put('/user/7/position',
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"},
				  data = json.dumps(JSON))
	
		
		self.assertEqual(rv.status_code,200)
