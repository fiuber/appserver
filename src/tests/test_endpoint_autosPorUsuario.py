from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.autosPorUsuario import AutosPorUsuario

def tirarExcepcion():
	raise Exception("")

def matchean(aux1, aux2):
	res = True
	try:

		res = res and (aux1["modelo"] == aux2["modelo"])
		res = res and (aux1["id"] == aux2["id"])
		res = res and (aux1["_ref"] == aux2["_ref"])
		res = res and (aux1["color"] == aux2["color"])
		res = res and (aux1["patente"] == aux2["patente"])
		res = res and (aux1["anio"] == aux2["anio"])
		res = res and (aux1["aireAcondicionado"] == aux2["aireAcondicionado"])
		res = res and (aux1["musica"] == aux2["musica"])

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

class TestEndpointAutosPorUsuario(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()



	@patch("src.resources.autosPorUsuario.mongo")	
	@patch("src.resources.autosPorUsuario.conectividad")
	@patch("src.resources.autosPorUsuario.Token")
	def test_camino_feliz(self, mockToken, mockConectividad, mockMongo):


		mockMongo.return_value = {"autoActivo": "3"}

		datosServer = {"cars": [
					{
					    "id": "1",
					    "_ref": "143.67298574212217",
					    "owner": "7",
					    "properties": []
					},
					{
					    "id": "2",
					    "_ref": "278.2764397976327",
					    "owner": "7",
					    "properties": [{"name": "modelo","value": "1999"},
						{"name": "color","value": "Azul"},
						{"name": "patente","value": "222222"},
						{"name": "anio","value": "2001"},
						{"name": "estado","value": "hecho mierda"},
						{"name": "aireAcondicionado","value": "ni en pedo"},
						{"name": "musica","value": "cumbia villera"}]
					},
					{
					    "id": "3",
					    "_ref": "278.65468547985468",
					    "owner": "7",
					    "properties": [{"name": "modelo","value": "DMC-12"},
						{"name": "color","value": "Gris"},
						{"name": "patente","value": "20CALIFORNIA15"},
						{"name": "anio","value": "1981"},
						{"name": "estado","value": "Impecable"},
						{"name": "aireAcondicionado","value": "No"},
						{"name": "musica","value": "Soundtrack de peliculas"}]
					}],
				    "metadata": {
					"version": "1"
				    }
				}

		loQueEsperoQueDevuelva =  {"1":
						{
						"_ref": "143.67298574212217",
						"id": "1"						
					    	},


					   "2": {
						"_ref": "278.2764397976327",
						"aireAcondicionado": "ni en pedo",
						"id": "2",
						"anio": "2001",
						"color": "Azul",
						"estado": "hecho mierda",
						"modelo": "1999",
						"musica": "cumbia villera",
						"patente": "222222"
					    	},


					    "3": {
						"_ref": "278.65468547985468",
						"aireAcondicionado": "No",
						"id": "3",
						"anio": "1981",
						"color": "Gris",
						"estado": "Impecable",
						"modelo": "DMC-12",
						"musica": "Soundtrack de peliculas",
						"patente": "20CALIFORNIA15"
					    	}
					  }



		mockConectividad.get.return_value = json.loads(json.dumps(datosServer))
		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/3/cars',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		jsonRV = json.loads(rv.data)
		
		self.assertTrue(jsonIguales(jsonRV, loQueEsperoQueDevuelva))

	@patch("src.resources.autosPorUsuario.mongo")	
	@patch("src.resources.autosPorUsuario.conectividad")
	@patch("src.resources.autosPorUsuario.Token")
	def test_sin_token(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = {"autoActivo": "3"}
		mockConectividad.get.return_value = True
		mockToken.return_value.validarToken.return_value = True
		
		rv = self.app.get('/driver/3/cars')

		self.assertEqual(rv.status_code,403)

	
	@patch("src.resources.autosPorUsuario.mongo")	
	@patch("src.resources.autosPorUsuario.conectividad")
	@patch("src.resources.autosPorUsuario.Token")
	def test_token_invalido(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = {"autoActivo": "3"}
		mockConectividad.get.return_value = True
		mockToken.return_value.validarToken.return_value = False

		rv = self.app.get('/driver/3/cars',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.autosPorUsuario.mongo")	
	@patch("src.resources.autosPorUsuario.conectividad")
	@patch("src.resources.autosPorUsuario.Token")
	def test_conexion_fallida(self, mockToken, mockConectividad, mockMongo):

		mockMongo.return_value = {"autoActivo": "3"}
		mockConectividad.get.return_value = False
		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/3/cars',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})

		self.assertEqual(rv.status_code, 404)
