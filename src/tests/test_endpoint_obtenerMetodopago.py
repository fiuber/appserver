from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.obtenerMetodoPago import ObtenerMetodoPago

def tirarExcepcion():
	raise Exception("")

def matchean(aux1, aux2):
	res = True
	try:
		res = res = res and (aux1.get("seleccionado", True) == aux2.get("seleccionado", True))
		res = res and (aux1.get("cvv", True) == aux2.get("cvv", True))
		res = res and (aux1.get("moneda", True) == aux2.get("moneda", True))
		res = res and (aux1.get("fechaNacimiento", True) == aux2.get("fechaNacimiento", True))
		res = res and (aux1.get("numero", True) == aux2.get("numero", True))

	except Exception as e:
		pass

	return res

def matcheaAlguno(aux1, aux2):
	res = False
	for auto in aux2:
		res = res or matchean(aux1, aux2[auto])	

	return res

def jsonIguales(j1, j2):
	res = True
	for auto in j1:
		res = res and matcheaAlguno(j1[auto], j2) 

	return res

class TestEndpointObtenerMetodopago(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()
		self.salidaCorrecta = {"tarjeta": {  "cvv": "1234",
						    "moneda": "pesos",
						    "fechaVencimiento": "12-2021",
						    "numero": "123456789"
						},
						"efectivo":{
							"moneda": "ARS"
						}}



	@patch("src.resources.obtenerMetodoPago.mongo")	
	@patch("src.resources.obtenerMetodoPago.Token")
	def test_camino_feliz(self, mockToken, mockMongo):



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

		
		rv = self.app.get('/users/3/metodopago',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
		jsonRV = json.loads(rv.data)
		
		self.assertTrue(jsonIguales(jsonRV, self.salidaCorrecta))


