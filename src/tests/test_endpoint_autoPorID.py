from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.autoPorID import AutoPorID

def tirarExcepcion():
	raise Exception("")

def jsonIguales(j1, j2):

	res = True

	res = res and (j1['modelo'] == j2['modelo'])
	res = res and (j1["color"] == j2["color"])
	res = res and (j1["patente"] == j2["patente"])
	res = res and (j1["anio"] == j2["anio"])
	res = res and (j1["aireAcondicionado"] == j2["aireAcondicionado"])
	res = res and (j1["musica"] == j2["musica"])
	return res

class TestEndpointAutoPorID(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()



	@patch("src.resources.autoPorID.Conectividad")
	@patch("src.resources.autoPorID.Token")
	def test_camino_feliz(self, mockToken, mockConectividad):


		datosAuto = {   "modelo": "2001",
		        	"color": "Azul",
				"patente": "ABC-001",
				"anio": "2001",
				"estado": "hecho mierda",
				"aireAcondicionado": "ni en pedo",
				"musica": "cumbia villera"}

		mockConectividad.return_value.get.return_value = json.loads(json.dumps(datosAuto))
		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		jsonRV = json.loads(rv.data)
		
		self.assertTrue(jsonIguales(jsonRV, datosAuto))


	@patch("src.resources.autoPorID.Conectividad")
	@patch("src.resources.autoPorID.Token")
	def test_sin_token(self, mockToken, mockConectividad):

		mockConectividad.return_value.get.return_value = True
		mockToken.return_value.validarToken.return_value = True
		
		rv = self.app.get('/driver/3/cars/8')

		self.assertEqual(rv.status_code,403)

	
	@patch("src.resources.autoPorID.Conectividad")
	@patch("src.resources.autoPorID.Token")
	def test_token_invalido(self, mockToken, mockConectividad):

		mockConectividad.return_value.get.return_value = True
		mockToken.return_value.validarToken.return_value = False

		rv = self.app.get('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.autoPorID.Conectividad")
	@patch("src.resources.autoPorID.Token")
	def test_conexion_fallida(self, mockToken, mockConectividad):

		mockConectividad.return_value.get.return_value = False
		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/3/cars/8',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 404)