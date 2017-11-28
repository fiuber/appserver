from mock import patch, MagicMock, PropertyMock
import unittest
import jwt
import src.server
import json

from src.resources.rutaEntrePuntos import RutaEntrePuntos

class TestEndpointRutaEntrePuntos(unittest.TestCase):
	
	def setUp(self):
		src.server.app.testing = True
		self.app = src.server.app.test_client()
		self.datosDirections = {
					   "routes" : [
					      {
						 "legs" : [
						    {
						       "distance" : {
							  "text" : "541 km",
							  "value" : 540551
						       },
						       "duration" : {
							  "text" : "5h 20 min",
							  "value" : 19216
						       },
						       "end_address" : "Montreal, Quebec, Canada",
						       "end_location" : {
							  "lat" : 45.5017123,
							  "lng" : -73.5672184
						       },
						       "start_address" : "Toronto, Ontario, Canada",
						       "start_location" : {
							  "lat" : 43.6533096,
							  "lng" : -79.3827656
						       },
						       "steps" : [
							  {
							     "distance" : {
								"text" : "0,3 km",
								"value" : 280
							     },
							     "duration" : {
								"text" : "1 min",
								"value" : 72
							     },
							     "end_location" : {
								"lat" : 43.6557259,
								"lng" : -79.38373369999999
							     },
							     "start_location" : {
								"lat" : 43.6533096,
								"lng" : -79.3827656
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "2,5 km",
								"value" : 2492
							     },
							     "duration" : {
								"text" : "9 min",
								"value" : 541
							     },
							     "end_location" : {
								"lat" : 43.6618361,
								"lng" : -79.35452389999999
							     },
							     "start_location" : {
								"lat" : 43.6557259,
								"lng" : -79.38373369999999
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "0,2 km",
								"value" : 220
							     },
							     "duration" : {
								"text" : "1 min",
								"value" : 22
							     },
							     "end_location" : {
								"lat" : 43.66366379999999,
								"lng" : -79.3555052
							     },
							     "start_location" : {
								"lat" : 43.6618361,
								"lng" : -79.35452389999999
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "12,9 km",
								"value" : 12897
							     },
							     "duration" : {
								"text" : "9 min",
								"value" : 563
							     },
							     "end_location" : {
								"lat" : 43.7628257,
								"lng" : -79.33669689999999
							     },
							     "start_location" : {
								"lat" : 43.66366379999999,
								"lng" : -79.3555052
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "1,1 km",
								"value" : 1070
							     },
							     "duration" : {
								"text" : "1 min",
								"value" : 50
							     },
							     "end_location" : {
								"lat" : 43.7680179,
								"lng" : -79.3292728
							     },
							     "start_location" : {
								"lat" : 43.7628257,
								"lng" : -79.33669689999999
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "23,0 km",
								"value" : 22987
							     },
							     "duration" : {
								"text" : "12 min",
								"value" : 730
							     },
							     "end_location" : {
								"lat" : 43.83811679999999,
								"lng" : -79.07197540000001
							     },
							     "start_location" : {
								"lat" : 43.7680179,
								"lng" : -79.3292728
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "319 km",
								"value" : 318830
							     },
							     "duration" : {
								"text" : "2h 51 min",
								"value" : 10266
							     },
							     "end_location" : {
								"lat" : 44.7393229,
								"lng" : -75.50066799999999
							     },
							     "start_location" : {
								"lat" : 43.83811679999999,
								"lng" : -79.07197540000001
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "109 km",
								"value" : 108807
							     },
							     "duration" : {
								"text" : "1h 0 min",
								"value" : 3588
							     },
							     "end_location" : {
								"lat" : 45.2083667,
								"lng" : -74.3482841
							     },
							     "start_location" : {
								"lat" : 44.7393229,
								"lng" : -75.50066799999999
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "67,3 km",
								"value" : 67288
							     },
							     "duration" : {
								"text" : "46 min",
								"value" : 2735
							     },
							     "end_location" : {
								"lat" : 45.4623177,
								"lng" : -73.6095157
							     },
							     "start_location" : {
								"lat" : 45.2083667,
								"lng" : -74.3482841
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "0,2 km",
								"value" : 226
							     },
							     "duration" : {
								"text" : "1 min",
								"value" : 12
							     },
							     "end_location" : {
								"lat" : 45.4635675,
								"lng" : -73.60723279999999
							     },
							     "start_location" : {
								"lat" : 45.4623177,
								"lng" : -73.6095157
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "0,8 km",
								"value" : 837
							     },
							     "duration" : {
								"text" : "1 min",
								"value" : 72
							     },
							     "end_location" : {
								"lat" : 45.4685691,
								"lng" : -73.59926759999999
							     },
							     "start_location" : {
								"lat" : 45.4635675,
								"lng" : -73.60723279999999
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "2,3 km",
								"value" : 2331
							     },
							     "duration" : {
								"text" : "2 min",
								"value" : 140
							     },
							     "end_location" : {
								"lat" : 45.4853231,
								"lng" : -73.5827443
							     },
							     "start_location" : {
								"lat" : 45.4685691,
								"lng" : -73.59926759999999
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "0,8 km",
								"value" : 847
							     },
							     "duration" : {
								"text" : "1 min",
								"value" : 73
							     },
							     "end_location" : {
								"lat" : 45.4911521,
								"lng" : -73.57746179999999
							     },
							     "start_location" : {
								"lat" : 45.4853231,
								"lng" : -73.5827443
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "1,4 km",
								"value" : 1424
							     },
							     "duration" : {
								"text" : "6 min",
								"value" : 339
							     },
							     "end_location" : {
								"lat" : 45.5018118,
								"lng" : -73.56734449999999
							     },
							     "start_location" : {
								"lat" : 45.4911521,
								"lng" : -73.57746179999999
							     },
							     "travel_mode" : "DRIVING"
							  },
							  {
							     "distance" : {
								"text" : "15 m",
								"value" : 15
							     },
							     "duration" : {
								"text" : "1 min",
								"value" : 13
							     },
							     "end_location" : {
								"lat" : 45.5017123,
								"lng" : -73.5672184
							     },
							     "start_location" : {
								"lat" : 45.5018118,
								"lng" : -73.56734449999999
							     },
							     "travel_mode" : "DRIVING"
							  }
						       ],
						       "traffic_speed_entry" : [],
						       "via_waypoint" : []
						    }
						 ]
		
					      }
					   ],
					   "status" : "OK"
					}
	
	@patch("src.resources.rutaEntrePuntos.conectividad")
	@patch("src.resources.rutaEntrePuntos.Token")
	def test_camino_feliz(self, mockToken, mockConectividad):

		mockConectividad.get.return_value = self.datosDirections

		mockToken.return_value.validarToken.return_value = True

		
		rv = self.app.get('/direction?origen=30.25&destino=89.1234967',
				  headers = {"Authorization": "Bearer jhvbdsfbhjbjfgjbeg43gbfbgfgfb"})
		
		self.assertEqual(rv.status_code,200)
	

