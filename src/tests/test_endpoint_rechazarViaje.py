from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.rechazarViaje import RechazarViaje


class TestEndpointRechazarViaje(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()

	@patch("src.resources.rechazarViaje.enviarNotificacionPush")
	@patch("src.resources.rechazarViaje.mongo")	
	@patch("src.resources.rechazarViaje.Token")
	def test_camino_feliz(self, mockToken, mockMongo, mockPush):

		mockPush.return_value = True
		mockToken.return_value.validarToken.return_value = True
		mockMongo.db.conductores.update.return_value = True
		mockMongo.db.conductores.find_one.return_value = {"viajes": [{"datosPasajero": {"idPasajero": "1"}}]}
		
		rv = self.app.delete('/driver/3/trip/1',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
		
		self.assertEqual(rv.status_code, 200)


