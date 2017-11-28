from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.eliminarMetodoPago import EliminarMetodoPago


class TestEndpointEliminarMetodopago(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()



	@patch("src.resources.eliminarMetodoPago.mongo")	
	@patch("src.resources.eliminarMetodoPago.Token")
	def test_camino_feliz_borrado_seleccionado(self, mockToken, mockMongo):


		JSON = {"metodo": "tarjeta"}

		mockMongo.db.usuarios.find_one.return_value = {"nombreUsuario": "pasajeroAgus",
								    "estado": "esperandoChofer",
								    "id": "1",
								    "posicion": {
									"lat": 3817522.310517724,
									"lng": 6512947.740492303
								    },
								    "metodopago": {
									"seleccionado": "tarjeta",
									"tarjeta": {
									    "cvv": "1234",
									    "moneda": "pesos",
									    "fechaVencimiento": "12-2021",
									    "numero": "123456789"
									},
									"efectivo":{
										"moneda": "ARS"
									}	
								    }
								}

		

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.delete('/users/3/metodopago',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"},
				  data = json.dumps(JSON),
				  content_type = "application/json")

		
		self.assertEqual(rv.status_code,200)


	@patch("src.resources.eliminarMetodoPago.mongo")	
	@patch("src.resources.eliminarMetodoPago.Token")
	def test_camino_feliz_borrado_ultimo_metodo(self, mockToken, mockMongo):


		JSON = {"metodo": "efectivo"}

		mockMongo.db.usuarios.find_one.return_value = {"nombreUsuario": "pasajeroAgus",
								    "estado": "esperandoChofer",
								    "id": "1",
								    "posicion": {
									"lat": 3817522.310517724,
									"lng": 6512947.740492303
								    },
								    "metodopago": {
									"seleccionado": "efectivo",
									"efectivo":{
										"moneda": "ARS"
									}	
								    }
								}

		

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.delete('/users/3/metodopago',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"},
				  data = json.dumps(JSON),
				  content_type = "application/json")

		
		self.assertEqual(rv.status_code,200)
