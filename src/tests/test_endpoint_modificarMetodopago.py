from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.modificarMetodoPago import ModificarMetodoPago


class TestEndpointModificarMetodopago(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()



	@patch("src.resources.modificarMetodoPago.mongo")	
	@patch("src.resources.modificarMetodoPago.Token")
	def test_camino_feliz_tarjeta(self, mockToken, mockMongo):


		JSON = {"metodo": "tarjeta",
				"parametros":{
					"moneda": "ARS",
					"numero": "123456789",
					"fechaVencimiento": "12-12-12",
					"cvv": "87564564-5656"
				}
			}

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
									}
								    }
								}

		

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.put('/users/3/metodopago',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"},
				  data = json.dumps(JSON),
				  content_type = "application/json")

		
		self.assertEqual(rv.status_code,200)

	@patch("src.resources.modificarMetodoPago.mongo")	
	@patch("src.resources.modificarMetodoPago.Token")
	def test_camino_feliz_efectivo(self, mockToken, mockMongo):


		JSON = {"metodo": "efectivo",
				"parametros":{
					"moneda": "ARS",
				}
			}

		mockMongo.db.usuarios.find_one.return_value = {"nombreUsuario": "pasajeroAgus",
								    "estado": "esperandoChofer",
								    "id": "1",
								    "posicion": {
									"lat": 3817522.310517724,
									"lng": 6512947.740492303
								    }
								}

		

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.put('/users/3/metodopago',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"},
				  data = json.dumps(JSON),
				  content_type = "application/json")

		
		self.assertEqual(rv.status_code,200)

