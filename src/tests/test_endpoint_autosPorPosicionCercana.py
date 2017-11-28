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
	res = res and (aux1["perfil"]["modelo"] == aux2["perfil"]["modelo"])
	res = res and (aux1["perfil"]["color"] == aux2["perfil"]["color"])
	res = res and (aux1["perfil"]["patente"] == aux2["perfil"]["patente"])
	res = res and (aux1["perfil"]["anio"] == aux2["perfil"]["anio"])
	res = res and (aux1["perfil"]["estado"] == aux2["perfil"]["estado"])
	res = res and (aux1["perfil"]["aireAcondicionado"] == aux2["perfil"]["aireAcondicionado"])
	res = res and (aux1["perfil"]["musica"] == aux2["perfil"]["musica"])
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

	@patch("src.resources.autosPorPosicionCercana.conectividad")
	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_camino_feliz(self, mockToken, mockPyMongo, mockConectividad):

		datosAutosShared = {"car": {
					"id": "4",
					"_ref": "278.2764397976327",
					"owner": "7",
					"properties": [{"name": "modelo","value": "1999"},
					    {"name": "color","value": "Azul"},
					    {"name": "patente","value": "222222"},
					    {"name": "anio","value": "2001"},
					    {"name": "estado","value": "hecho mierda"},
					    {"name": "aireAcondicionado","value": "ni en pedo"},
					    {"name": "musica","value": "cumbia villera"}
					]
				    },
				    "metadata": {
					"version": "1"
				    }
				}


		datosAuto1 = {"id": "4",
			      "perfil":{"modelo": "1999",
					"color": "Azul",
					"patente": "222222",
					"anio": "2001",
					"estado": "hecho mierda",
					"aireAcondicionado": "ni en pedo",
					"musica": "cumbia villera"}
			     }

		mockConectividad.get.return_value = datosAutosShared

		datosAutos = [datosAuto1, datosAuto1]
		jsonDatosAutos = {"1": datosAutos[0], "2": datosAutos[1]}

		mockFind = MagicMock()
		mockFind.find.return_value = datosAutos

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		mockPyMongo.db.conductores.find_one.return_value = {"autoActivo": "4", "id": "189"}

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/search',
				  query_string = {"lng": "3", "lat": "3"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		jsonRV = json.loads(rv.data)
		print(str(rv.data))
		
		self.assertTrue(jsonIguales(jsonRV, jsonDatosAutos))

	@patch("src.resources.autosPorPosicionCercana.conectividad")
	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_sin_lat_y_lng(self, mockToken, mockPyMongo, mockConectividad):


		mockToken.return_value.validarToken.return_value = True

		mockFind = MagicMock()
		mockFind.find.return_value = False

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		
		rv = self.app.get('/driver/search',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		
		self.assertEqual(rv.status_code, 404)

	@patch("src.resources.autosPorPosicionCercana.conectividad")
	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_sin_token(self, mockToken, mockPyMongo, mockConectividad):

		
		mockToken.return_value.validarToken.return_value = False

		mockFind = MagicMock()
		mockFind.find.return_value = False

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	
		
		rv = self.app.get('/driver/search',
				  query_string = {"lng": "3", "lat": "3"})
		
		self.assertEqual(rv.status_code, 403)


	@patch("src.resources.autosPorPosicionCercana.conectividad")	
	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_token_invalido(self, mockToken, mockPyMongo, mockConectividad):

		mockToken.return_value.validarToken.return_value = False

		mockFind = MagicMock()
		mockFind.find.return_value = False

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		rv = self.app.get('/driver/search',
				  query_string = {"lng": "3", "lat": "3"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.autosPorPosicionCercana.conectividad")
	@patch("src.resources.autosPorPosicionCercana.mongo")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_conexion_fallida(self, mockToken, mockPyMongo, mockConectividad):

		mockToken.return_value.validarToken.return_value = True

		mockFind = MagicMock()
		mockFind.find.return_value = tirarExcepcion

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	
		
		rv = self.app.get('/driver/search',
		                  query_string = {"lng": "3", "lat": "3"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 403)
