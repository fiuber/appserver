from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.aceptarViaje import AceptarViaje

def tirarExcepcion():
	raise Exception("")

class TestEndpointAceptarViaje(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()
		self.jsonDatosConductor = {
		    "_id": {
			"$oid": "5a0240caf36d28476ec09c27"
		    },
		    "nombreUsuario": "MarcosDriver",
		    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmVVc3VhcmlvIjoiTWFyY29zRHJpdmVyIiwiaWF0IjoxNTEwMDg5MDY2LCJjb250cmFzZW5hIjoiUGVybmljYSIsImV4cCI6MTUxMDE3NTQ2Nn0.hcfly9-0_euM-MkaWs9q9tYCYAIp6dzD-OO97bKJHtc",
		    "estado": "libre",
		    "id": "5",
		    "contadorViajes": 14,
		    "viajes": [
			{
			    "idViaje": "14",
			    "datosPasajero": {
				"nombreUsuario": "Marcos",
				"apellido": "Pernica",
				"idPasajero": "3",
				"pais": "Argentina",
				"nombre": "Marcos",
				"imagenes": [
				    "1.png",
				    "2.png",
				    "3.png"
				],
				"email": "Tu vieja.com",
				"fechaNacimiento": "12 12 123"
			    },
			    "costo": "0",
			    "ruta": {
				"ruta": {
				    "11": {
				        "fin": {
				            "lat": 42.458195,
				            "lng": -71.343842
				        },
				        "inicio": {
				            "lat": 42.4498381,
				            "lng": -71.3200351
				        }
				    },
				    "10": {
				        "fin": {
				            "lat": 42.4498381,
				            "lng": -71.3200351
				        },
				        "inicio": {
				            "lat": 42.4486492,
				            "lng": -71.3169614
				        }
				    },
				    "13": {
				        "fin": {
				            "lat": 42.46078600000001,
				            "lng": -71.348839
				        },
				        "inicio": {
				            "lat": 42.4602875,
				            "lng": -71.348514
				        }
				    },
				    "12": {
				        "fin": {
				            "lat": 42.4602875,
				            "lng": -71.348514
				        },
				        "inicio": {
				            "lat": 42.458195,
				            "lng": -71.343842
				        }
				    },
				    "15": {
				        "fin": {
				            "lat": 42.460387,
				            "lng": -71.3489306
				        },
				        "inicio": {
				            "lat": 42.4614275,
				            "lng": -71.3493778
				        }
				    },
				    "14": {
				        "fin": {
				            "lat": 42.4614275,
				            "lng": -71.3493778
				        },
				        "inicio": {
				            "lat": 42.46078600000001,
				            "lng": -71.348839
				        }
				    },
				    "1": {
				        "fin": {
				            "lat": 42.3624195,
				            "lng": -71.0585323
				        },
				        "inicio": {
				            "lat": 42.360989,
				            "lng": -71.0611984
				        }
				    },
				    "0": {
				        "fin": {
				            "lat": 42.360989,
				            "lng": -71.0611984
				        },
				        "inicio": {
				            "lat": 42.3598335,
				            "lng": -71.0598776
				        }
				    },
				    "3": {
				        "fin": {
				            "lat": 42.3741949,
				            "lng": -71.0710391
				        },
				        "inicio": {
				            "lat": 42.36317589999999,
				            "lng": -71.0569388
				        }
				    },
				    "2": {
				        "fin": {
				            "lat": 42.36317589999999,
				            "lng": -71.0569388
				        },
				        "inicio": {
				            "lat": 42.3624195,
				            "lng": -71.0585323
				        }
				    },
				    "5": {
				        "fin": {
				            "lat": 42.4147393,
				            "lng": -71.1313878
				        },
				        "inicio": {
				            "lat": 42.4081604,
				            "lng": -71.1012071
				        }
				    },
				    "4": {
				        "fin": {
				            "lat": 42.4081604,
				            "lng": -71.1012071
				        },
				        "inicio": {
				            "lat": 42.3741949,
				            "lng": -71.0710391
				        }
				    },
				    "7": {
				        "fin": {
				            "lat": 42.4290309,
				            "lng": -71.2601121
				        },
				        "inicio": {
				            "lat": 42.3982572,
				            "lng": -71.1416168
				        }
				    },
				    "6": {
				        "fin": {
				            "lat": 42.3982572,
				            "lng": -71.1416168
				        },
				        "inicio": {
				            "lat": 42.4147393,
				            "lng": -71.1313878
				        }
				    },
				    "9": {
				        "fin": {
				            "lat": 42.4486492,
				            "lng": -71.3169614
				        },
				        "inicio": {
				            "lat": 42.4306134,
				            "lng": -71.2631636
				        }
				    },
				    "8": {
				        "fin": {
				            "lat": 42.4306134,
				            "lng": -71.2631636
				        },
				        "inicio": {
				            "lat": 42.4290309,
				            "lng": -71.2601121
				        }
				    }
				},
				"distancia": 31600
			    },
			    "destino": {
				"lat": 42.460387,
				"lng": -71.3489306
			    },
			    "origen": {
				"lat": 42.3598335,
				"lng": -71.0598776
			    }
			}
		    ]
		} 


	@patch("src.resources.aceptarViaje.mongo")
	@patch("src.resources.aceptarViaje.Token")
	def test_camino_feliz(self, mockToken, mockPyMongo):


		mockUpdateCli = MagicMock()
		mockUpdateCli.update.return_value = {"nModified": 1}


		mockInsertViaje = MagicMock()
		mockInsertViaje.insert.return_value = {}

		MockConductores = MagicMock()
		MockConductores.find_one.return_value = self.jsonDatosConductor
		MockConductores.update.return_value = {"nModified": 1}

		p = PropertyMock(return_value = MockConductores)
		type(mockPyMongo.db).conductores = p  	

		p2 = PropertyMock(return_value = mockUpdateCli)
		type(mockPyMongo.db).usuarios = p2  	


		p4 = PropertyMock(return_value = mockInsertViaje)
		type(mockPyMongo.db).viajes = p4  	

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.post('/driver/7/trip/10',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
		
		self.assertEqual(rv.status_code,200)


	@patch("src.resources.aceptarViaje.mongo")
	@patch("src.resources.aceptarViaje.Token")
	def test_token_invalido(self, mockToken, mockPyMongo):

		mockToken.return_value.validarToken.return_value = False

	
		rv = self.app.post('/driver/7/trip/10',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
	
		self.assertEqual(rv.status_code,400)

	@patch("src.resources.aceptarViaje.mongo")
	@patch("src.resources.aceptarViaje.Token")
	def test_excepcion_viajes_find(self, mockToken, mockPyMongo):
	

		mockUpdateCli = MagicMock()
		mockUpdateCli.update.return_value = {"nModified": 1}


		mockInsertViaje = MagicMock()
		mockInsertViaje.insert.side_effect = tirarExcepcion

		MockConductores = MagicMock()
		MockConductores.find_one.return_value = self.jsonDatosConductor
		MockConductores.update.return_value = {"nModified": 1}

		p = PropertyMock(return_value = MockConductores)
		type(mockPyMongo.db).conductores = p  	

		p2 = PropertyMock(return_value = mockUpdateCli)
		type(mockPyMongo.db).usuarios = p2  	


		p4 = PropertyMock(return_value = mockInsertViaje)
		type(mockPyMongo.db).viajes = p4  	

		mockToken.return_value.validarToken.return_value = True

	
		rv = self.app.post('/driver/7/trip/10',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
	
		self.assertEqual(rv.status_code,400)

	@patch("src.resources.aceptarViaje.mongo")
	@patch("src.resources.aceptarViaje.Token")
	def test_usuario_inexistente(self, mockToken, mockPyMongo):
	

		mockUpdateCli = MagicMock()
		mockUpdateCli.update.return_value = {"nModified": 0}


		mockInsertViaje = MagicMock()
		mockInsertViaje.insert.return_value = {}

		MockConductores = MagicMock()
		MockConductores.find_one.return_value = self.jsonDatosConductor
		MockConductores.update.return_value = {"nModified": 1}

		p = PropertyMock(return_value = MockConductores)
		type(mockPyMongo.db).conductores = p  	

		p2 = PropertyMock(return_value = mockUpdateCli)
		type(mockPyMongo.db).usuarios = p2  	


		p4 = PropertyMock(return_value = mockInsertViaje)
		type(mockPyMongo.db).viajes = p4  	

		mockToken.return_value.validarToken.return_value = True

	
		rv = self.app.post('/driver/7/trip/10',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
	
		self.assertEqual(rv.status_code,400)

	@patch("src.resources.aceptarViaje.mongo")
	@patch("src.resources.aceptarViaje.Token")
	def test_conductor_inexistente(self, mockToken, mockPyMongo):
	

		mockUpdateCli = MagicMock()
		mockUpdateCli.update.return_value = {"nModified": 0}


		mockInsertViaje = MagicMock()
		mockInsertViaje.insert.return_value = {}

		MockConductores = MagicMock()
		MockConductores.find_one.return_value = {}
		MockConductores.update.return_value = {"nModified": 1}

		p = PropertyMock(return_value = MockConductores)
		type(mockPyMongo.db).conductores = p  	

		p2 = PropertyMock(return_value = mockUpdateCli)
		type(mockPyMongo.db).usuarios = p2  	


		p4 = PropertyMock(return_value = mockInsertViaje)
		type(mockPyMongo.db).viajes = p4  	

		mockToken.return_value.validarToken.return_value = True

	
		rv = self.app.post('/driver/7/trip/10',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
	
		self.assertEqual(rv.status_code,400)

	@patch("src.resources.aceptarViaje.mongo")
	@patch("src.resources.aceptarViaje.Token")
	def test_update_fallido_con_excepcion(self, mockToken, mockPyMongo):
	

		mockUpdateCli = MagicMock()
		mockUpdateCli.update.return_value = {"nModified": 0}


		mockInsertViaje = MagicMock()
		mockInsertViaje.insert.return_value = {}

		MockConductores = MagicMock()
		MockConductores.find_one.return_value = tirarExcepcion
		MockConductores.update.return_value = {}

		p = PropertyMock(return_value = MockConductores)
		type(mockPyMongo.db).conductores = p  	

		p2 = PropertyMock(return_value = mockUpdateCli)
		type(mockPyMongo.db).usuarios = p2  	


		p4 = PropertyMock(return_value = mockInsertViaje)
		type(mockPyMongo.db).viajes = p4  	

		mockToken.return_value.validarToken.return_value = True

	
		rv = self.app.post('/driver/7/trip/10',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
	
		self.assertEqual(rv.status_code,403)


