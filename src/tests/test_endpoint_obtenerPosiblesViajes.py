from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.obtenerPosiblesViajes import ObtenerPosiblesViajes

def tirarExcepcion():
	raise Exception("")

def matchean(aux1, aux2):
	res = True
	res = res and (aux1["idViaje"] == aux2["idViaje"])
	res = res and (aux1["datosPasajero"]["nombreUsuario"] == aux2["datosPasajero"]["nombreUsuario"])
	res = res and (aux1["datosPasajero"]["apellido"] == aux2["datosPasajero"]["apellido"])
	res = res and (aux1["datosPasajero"]["idPasajero"] == aux2["datosPasajero"]["idPasajero"])
	res = res and (aux1["datosPasajero"]["pais"] == aux2["datosPasajero"]["pais"])
	res = res and (aux1["datosPasajero"]["nombre"] == aux2["datosPasajero"]["nombre"])
	res = res and (aux1["datosPasajero"]["email"] == aux2["datosPasajero"]["email"])
	res = res and (aux1["datosPasajero"]["fechaNacimiento"] == aux2["datosPasajero"]["fechaNacimiento"])
	res = res and (aux1["ruta"]["distancia"] == aux2["ruta"]["distancia"])

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

class TestEndpointObtenerPosiblesViajes(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()
		self.viajesDisponibles = { "viajes": [{
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
			},{
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
			},{
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
			}]}

		self.salidaCorrecta = {"0": {
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
				}, 
				"1": {
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
				}} 


	@patch("src.resources.obtenerPosiblesViajes.Conectividad")
	@patch("src.resources.obtenerPosiblesViajes.mongo")
	@patch("src.resources.obtenerPosiblesViajes.Token")
	def test_camino_feliz(self, mockToken, mockPyMongo, mockConectividad):

		mockFind = MagicMock()
		mockFind.find_one.return_value = self.viajesDisponibles


		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/7/trip',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
		
		jsonRV = json.loads(rv.data)
		
		self.assertTrue(jsonIguales(jsonRV, self.salidaCorrecta))

	@patch("src.resources.obtenerPosiblesViajes.Conectividad")
	@patch("src.resources.obtenerPosiblesViajes.mongo")
	@patch("src.resources.obtenerPosiblesViajes.Token")
	def test_token_invalido(self, mockToken, mockPyMongo, mockConectividad):

		mockFind = MagicMock()
		mockFind.find_one.return_value = self.viajesDisponibles


		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		mockToken.return_value.validarToken.return_value = False

		
		rv = self.app.get('/driver/7/trip',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
		
		jsonRV = json.loads(rv.data)
		
		self.assertEqual(rv.status_code, 400)

	@patch("src.resources.obtenerPosiblesViajes.Conectividad")
	@patch("src.resources.obtenerPosiblesViajes.mongo")
	@patch("src.resources.obtenerPosiblesViajes.Token")
	def test_conductor_inexistente(self, mockToken, mockPyMongo, mockConectividad):

		mockFind = MagicMock()
		mockFind.find_one.return_value = False


		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p  	

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/driver/7/trip',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
		
		jsonRV = json.loads(rv.data)
		
		self.assertEqual(rv.status_code, 400)
