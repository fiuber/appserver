from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.autosPorPosicionCercana import AutosPorPosicionCercana

def tirarExcepcion():
	raise Exception("")

def matchean(aux1, aux2):
	res = True
	res = res and (aux1["id"] == aux2["id"])
	res = res and (aux1["posicion"]["lng"] == aux2["posicion"]["lng"])
	res = res and (aux1["posicion"]["lat"] == aux2["posicion"]["lat"])
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

class TestEndpointAutosPorPosicionCercana(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()


	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_camino_feliz(self, mockToken, mockPyMongo):


		datosAuto1 = {"id": "4",
			      "posicion":{"lng": "45.876",
					  "lat": "50.6578"}
			     }

		datosAuto2 = {"id": "5",
			      "posicion":{"lng": "78.7876",
					  "lat": "32.6578"}
			     }

		datosAutos = [datosAuto1, datosAuto2]
		jsonDatosAutos = {"1": datosAutos[0], "2": datosAutos[1]}

		mockFind = MagicMock()
		mockFind.find.return_value = datosAutos

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/search',
				  query_string = {"lng": "3", "lat": "3"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		jsonRV = json.loads(rv.data)
		
		self.assertTrue(jsonIguales(jsonRV, jsonDatosAutos))

	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_sin_lat_y_lng(self, mockToken, mockPyMongo):


		mockToken.return_value.validarToken.return_value = True

		mockFind = MagicMock()
		mockFind.find.return_value = False

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		
		rv = self.app.get('/driver/search',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		
		self.assertEqual(rv.status_code, 404)

	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_sin_token(self, mockToken, mockPyMongo):

		
		mockToken.return_value.validarToken.return_value = False

		mockFind = MagicMock()
		mockFind.find.return_value = False

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	
		
		rv = self.app.get('/driver/search',
				  query_string = {"lng": "3", "lat": "3"})
		
		self.assertEqual(rv.status_code, 403)

	
	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_token_invalido(self, mockToken, mockPyMongo):

		mockToken.return_value.validarToken.return_value = False

		mockFind = MagicMock()
		mockFind.find.return_value = False

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		rv = self.app.get('/driver/search',
				  query_string = {"lng": "3", "lat": "3"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_conexion_fallida(self, mockToken, mockPyMongo):

		mockToken.return_value.validarToken.return_value = True

		mockFind = MagicMock()
		mockFind.find.return_value = tirarExcepcion

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	
		
		rv = self.app.get('/driver/search',
		                  query_string = {"lng": "3", "lat": "3"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 403)
