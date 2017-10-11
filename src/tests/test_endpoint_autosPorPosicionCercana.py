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
	res = res and (aux1["modelo"] == aux2["modelo"])
	res = res and (aux1["color"] == aux2["color"])
	res = res and (aux1["patente"] == aux2["patente"])
	res = res and (aux1["anio"] == aux2["anio"])
	res = res and (aux1["aireAcondicionado"] == aux2["aireAcondicionado"])
	res = res and (aux1["musica"] == aux2["musica"])

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



	@patch("src.resources.autosPorPosicionCercana.Conectividad")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_camino_feliz(self, mockToken, mockConectividad):


		datosAuto1 = {  "modelo": "2001",
		        	"color": "Azul",
				"patente": "ABC-001",
				"anio": "2001",
				"estado": "hecho mierda",
				"aireAcondicionado": "ni en pedo",
				"musica": "cumbia villera"}

		datosAuto2 = {  "modelo": "2002",
		        	"color": "Verde",
				"patente": "DEF-358",
				"anio": "4820",
				"estado": "tuneado con aleron (?)",
				"aireAcondicionado": "seeeee",
				"musica": "sountrack de rapido y furioso"}

		datosAutos = {"1": datosAuto1, "2": datosAuto2}
		metadata = {"count ": 2, "total": 2, "next": "sddsf", "prev": "jkdsfgf", "first": "jhdgdgs", "last": "fdsdf", "version": 1.0}
		datosServer = {"cars": datosAutos, "metadata": metadata }



		mockConectividad.return_value.get.return_value = json.loads(json.dumps(datosServer))
		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/search',
				  query_string = {"IDUsuario": "3"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		jsonRV = json.loads(rv.data)
		
		self.assertTrue(jsonIguales(jsonRV, datosAutos))

	@patch("src.resources.autosPorPosicionCercana.Conectividad")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_sin_IDUsuario(self, mockToken, mockConectividad):


		mockConectividad.return_value.get.return_value = True
		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/search',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		
		self.assertEqual(rv.status_code, 404)

	@patch("src.resources.autosPorPosicionCercana.Conectividad")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_sin_token(self, mockToken, mockConectividad):

		
		mockConectividad.return_value.get.return_value = False
		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/search',
				  query_string = {"IDUsuario": "2"})
		
		self.assertEqual(rv.status_code, 403)

	
	@patch("src.resources.autosPorPosicionCercana.Conectividad")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_token_invalido(self, mockToken, mockConectividad):

		mockConectividad.return_value.get.return_value = True
		mockToken.return_value.validarToken.return_value = False

		rv = self.app.get('/driver/search',
				  query_string = {"IDUsuario": "2"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.autosPorPosicionCercana.Conectividad")
	@patch("src.resources.autosPorPosicionCercana.Token")
	def test_conexion_fallida(self, mockToken, mockConectividad):

		mockConectividad.return_value.get.return_value = False
		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/search',
		                  query_string = {"IDUsuario": "2"},
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 404)
