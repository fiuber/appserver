from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.driverModificarPosicion import ConductorModificarPosicion

def tirarExcepcion():
	raise Exception("")


class TestEndpointDriverModificarPosicion(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()

	@patch("src.resources.driverModificarPosicion.Log")
	@patch("src.resources.driverModificarPosicion.conectividad")
	@patch("src.resources.driverModificarPosicion.mongo")
	@patch("src.resources.driverModificarPosicion.Token")
	def test_camino_feliz_viajando(self, mockToken, mockMongo, mockConectividad, mockLog):

		JSON = {
				"posicion":
				{
				"lat": 42.460387,
				"lng": -71.3489306
				}
			}

		mockMongo.db.viajes.find_one.return_value = {
								    "_id": {
									"$oid": "5a1d7f371434c9000fb9f615"
								    },
								    "origenGrados": {
									"lat": -34.4855239,
									"lng": -58.50686049999999
								    },
								    "IDPasajero": "1",
								    "timestampInicio": 1511882551.262059,
								    "IDConductor": "2",
								    "rutaConductor": [
									{
									    "timestamp": 1511882630.246073,
									    "location": {
										"lat": 3817494.2079510833,
										"lng": 6512946.998362365
									    }
									},
									{
									    "timestamp": 1511882676.651661,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6516099.380809122
									    }
									},
									{
									    "timestamp": 1511883020.308116,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6627418.871601557
									    }
									},
									{
									    "timestamp": 1511883025.646899,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6516099.380809122
									    }
									}
								    ],
								    "destino": {
									"lat": 3819071.9507099795,
									"lng": 6516100.308471543
								    },
								    "destinoGrados": {
									"lat": -34.4995227,
									"lng": -58.53512499999999
								    },
								    "timestampFinEspera": 12356678,
								    "origen": {
									"lat": 3817519.045443145,
									"lng": 6512953.9187240405
								    },
								    "timestampFinViaje": 0,
								    "rutaConductorGrados": [
									{
									    "timestamp": 1511882630.246073,
									    "location": {
										"lat": -34.4853,
										"lon": -58.506798333333336
									    }
									},
									{
									    "timestamp": 1511882676.651661,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -58.53511666666667
									    }
									},
									{
									    "timestamp": 1511883020.308116,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -59.53511666666667
									    }
									},
									{
									    "timestamp": 1511883025.646899,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -58.53511666666667
									    }
									}
								    ]
								}



		mockMongo.db.viajes.update.return_value = {"nModified": 1}
		mockMongo.db.conductores.find_and_modify.return_value = {  "nombreUsuario": "choferFranco",
									    "estado": "viajando",
									    "id": "2",
									    "autosRegistrados": [
										"1"
									    ],
									    "posicion": {
										"lat": 3817522.310517724,
										"lng": 6512947.740492303
									    },
									    "autoActivo": "1",
									    "contadorViajes": 14,
									    "viajes": []
									}

		mockMongo.db.usuarios.find_one.return_value = {"nombreUsuario": "pasajeroAgus",
								    "estado": "viajando",
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

		
		rv = self.app.put('/driver/7/position',
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"},
				  data = json.dumps(JSON))
	
		
		self.assertEqual(rv.status_code,200)

	@patch("src.resources.driverModificarPosicion.Log")
	@patch("src.resources.driverModificarPosicion.conectividad")
	@patch("src.resources.driverModificarPosicion.mongo")
	@patch("src.resources.driverModificarPosicion.Token")
	def test_camino_feliz_espera_terminada(self, mockToken, mockMongo, mockConectividad, mockLog):

		JSON = {
				"posicion":
				{
									"lat": -34.4855239,
									"lng": -58.50686049999999
				}
			}

		mockMongo.db.viajes.find_one.return_value = {"_id": {
									"$oid": "5a1d7f371434c9000fb9f615"
								    },
								    "origenGrados": {
									"lat": -34.4855239,
									"lng": -58.50686049999999
								    },
								    "IDPasajero": "1",
								    "timestampInicio": 1511882551.262059,
								    "IDConductor": "2",
								    "rutaConductor": [
									{
									    "timestamp": 1511882630.246073,
									    "location": {
										"lat": 3817494.2079510833,
										"lng": 6512946.998362365
									    }
									},
									{
									    "timestamp": 1511882676.651661,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6516099.380809122
									    }
									},
									{
									    "timestamp": 1511883020.308116,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6627418.871601557
									    }
									},
									{
									    "timestamp": 1511883025.646899,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6516099.380809122
									    }
									}
								    ],
								    "destino": {
									"lat": 3819071.9507099795,
									"lng": 6516100.308471543
								    },
								    "destinoGrados": {
									"lat": -34.4995227,
									"lng": -58.53512499999999
								    },
								    "timestampFinEspera": 0,
								    "origen": {
									"lat": 3817519.045443145,
									"lng": 6512953.9187240405
								    },
								    "timestampFinViaje": 0,
								    "rutaConductorGrados": [
									{
									    "timestamp": 1511882630.246073,
									    "location": {
										"lat": -34.4853,
										"lon": -58.506798333333336
									    }
									},
									{
									    "timestamp": 1511882676.651661,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -58.53511666666667
									    }
									},
									{
									    "timestamp": 1511883020.308116,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -59.53511666666667
									    }
									},
									{
									    "timestamp": 1511883025.646899,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -58.53511666666667
									    }
									}
								    ]
								}

		mockMongo.db.viajes.update.return_value = {"nModified": 1}
		mockMongo.db.usuarios.update.return_value = {"nModified": 1}
		mockMongo.db.conductores.update.return_value = {"nModified": 1}
		mockMongo.db.conductores.find_and_modify.return_value = {  "nombreUsuario": "choferFranco",
									    "estado": "recogiendoPasajero",
									    "id": "2",
									    "autosRegistrados": [
										"1"
									    ],
									    "posicion": {
										"lat": 3817522.310517724,
										"lng": 6512947.740492303
									    },
									    "autoActivo": "1",
									    "contadorViajes": 14,
									    "viajes": []
									}

		mockMongo.db.usuarios.find_one.return_value = {"nombreUsuario": "pasajeroAgus",
								    "estado": "esperandoChofer",
								    "id": "1",
								    "posicion": {
										"lat": 3817519.045443145,
										"lng": 6512953.9187240405
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

		
		rv = self.app.put('/driver/7/position',
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"},
				  data = json.dumps(JSON))
	
		
		self.assertEqual(rv.status_code,200)

	@patch("src.resources.driverModificarPosicion.enviarNotificacionPush")
	@patch("src.resources.driverModificarPosicion.Log")
	@patch("src.resources.driverModificarPosicion.conectividad")
	@patch("src.resources.driverModificarPosicion.mongo")
	@patch("src.resources.driverModificarPosicion.Token")
	def test_camino_feliz_viaje_terminado(self, mockToken, mockMongo, mockConectividad, mockLog, mockPush):

		JSON = {
				"posicion":
				{
					"lat": -34.4995227,
					"lng": -58.53512499999999
				}
			}

		mockPush = True
		mockMongo.db.viajes.find_one.return_value = {"_id": {
									"$oid": "5a1d7f371434c9000fb9f615"
								    },
								    "origenGrados": {
									"lat": -34.4855239,
									"lng": -58.50686049999999
								    },
								    "IDPasajero": "1",
								    "timestampInicio": 1511882551.262059,
								    "IDConductor": "2",
								    "rutaConductor": [
									{
									    "timestamp": 1511882630.246073,
									    "location": {
										"lat": 3817494.2079510833,
										"lng": 6512946.998362365
									    }
									},
									{
									    "timestamp": 1511882676.651661,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6516099.380809122
									    }
									},
									{
									    "timestamp": 1511883020.308116,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6627418.871601557
									    }
									},
									{
									    "timestamp": 1511883025.646899,
									    "location": {
										"lat": 3819075.34890978,
										"lng": 6516099.380809122
									    }
									}
								    ],
								    "destino": {
									"lat": 3819071.9507099795,
									"lng": 6516100.308471543
								    },
								    "destinoGrados": {
									"lat": -34.4995227,
									"lng": -58.53512499999999
								    },
								    "timestampFinEspera": 123465,
								    "origen": {
									"lat": 3817519.045443145,
									"lng": 6512953.9187240405
								    },
								    "timestampFinViaje": 0,
								    "rutaConductorGrados": [
									{
									    "timestamp": 1511882630.246073,
									    "location": {
										"lat": -34.4853,
										"lon": -58.506798333333336
									    }
									},
									{
									    "timestamp": 1511882676.651661,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -58.53511666666667
									    }
									},
									{
									    "timestamp": 1511883020.308116,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -59.53511666666667
									    }
									},
									{
									    "timestamp": 1511883025.646899,
									    "location": {
										"lat": 34.49955333333333,
										"lon": -58.53511666666667
									    }
									}
								    ]
								}

		mockMongo.db.viajes.update.return_value = {"nModified": 1}
		mockMongo.db.usuarios.update.return_value = {"nModified": 1}
		mockMongo.db.conductores.update.return_value = {"nModified": 1}
		mockMongo.db.conductores.find_and_modify.return_value = {  "nombreUsuario": "choferFranco",
									    "estado": "viajando",
									    "id": "2",
									    "autosRegistrados": [
										"1"
									    ],
									    "posicion": {
										"lat": 3817522.310517724,
										"lng": 6512947.740492303
									    },
									    "autoActivo": "1",
									    "contadorViajes": 14,
									    "viajes": []
									}

		mockMongo.db.usuarios.find_one.return_value = {"nombreUsuario": "pasajeroAgus",
								    "estado": "viajando",
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
		mockConectividad.post.return_value = True
		
		rv = self.app.put('/driver/7/position',
				  content_type = "application/json",
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"},
				  data = json.dumps(JSON))
	
		
		self.assertEqual(rv.status_code,200)


