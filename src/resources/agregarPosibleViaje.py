# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import time
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token
from src.models.conectividad import Conectividad
from geopy.distance import vincenty

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo
from src import directionsAPIKey
from src import URLGoogleDirections
from src import URLSharedServer
from src import origen

class AgregarPosibleViaje(Resource):
	"""!@brief Clase para agregar un viaje a la lista de posibles viajes de un chofer."""


	def __init__(self):
		self.autenticador = Token() 
		self.conectividad = Conectividad(URLSharedServer)

	def post(self, IDUsuario):
		"""!@brief Agrega la informacion del viaje posible."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el JSON con los datos del viaje."""
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")
			self.IDUsuario = IDUsuario

			"""Guarda el posible viaje en mongoDB."""
			datos = self._obtenerJSONViaje()
			if(not datos):
				return ErrorHandler.create_error_response(404, "Imposible obtener ruta.")

			if(not self._guardar_viaje_mongo(datos)):
				return ErrorHandler.create_error_response(404, "Imposible guardar datos de viaje.")

			self._informar_viaje(IDUsuario)

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response

	def _get_data_from_request(self, nombrePropiedad):
		"""!@brief Obtiene la propiedad del json contenido de la request."""
		
		try:
			return request.get_json()[nombrePropiedad]
		except Exception as e:
			return False

	def _validate_request(self):
		"""!@brief Valida que haya una request completa."""

		res = self._get_data_from_request("IDPasajero") and self._get_data_from_request("destino") and self._get_data_from_request("origen")

		if(not res):
			return False
		else:
			return True

	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = self.autenticador.validarToken(token)
		if(not res):
			return False
		return True

	def _obtener_costo_viaje(self, IDUsuario, IDPasajero, ruta):
		"""!@brief le pide al shared server la cotizacion del viaje."""

		self.conectividad.setURL(URLSharedServer)

		JSON = {"driver": IDUsuario,
			"passenger": IDPasajero,
			"start":{
				"address":{
					"location":{
						"lat": float(ruta["origen"]["lat"]),
						"lon": float(ruta["origen"]["lng"])
					}
				},
				"timestamp": time.time()
			},
			"end":{
				"address":{
					"location":{
						"lat": float(ruta["destino"]["lat"]),
						"lon": float(ruta["destino"]["lng"])
					}
				}
			},
			"distance": float(ruta["mongo"]["distancia"])
		}
		valor = self.conectividad.post("trips/estimate",JSON)
		
		if(not valor):
			raise Exception("Error en el Shared Server.")
		return valor["trip"]["cost"]["value"]

	def _obtenerJSONViaje(self):
		"""!@brief Obtiene toda la informacion y crea el JSON de datos del viaje."""


		"""Pide la informacion del usuario al Shared Server."""
		self.conectividad.setURL(URLSharedServer)
		datosUsuario = self.conectividad.get("users/"+self._get_data_from_request("IDPasajero"))
		if(not datosUsuario):
			return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")
		
		ruta = self._calcular_ruta(self._get_data_from_request("origen"), self._get_data_from_request("destino"))
		if(not ruta):
			return False

		"""Pide la cotizacion del viaje al Shared Server."""
		cotizacion = 0
		try:
			cotizacion = self._obtener_costo_viaje(self.IDUsuario, self._get_data_from_request("IDPasajero"), ruta)
		except Exception as e:
			return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

		
		"""Obtiene el ID de viaje a insertar"""		
		IDViaje = self._obtener_ID_viaje(self.IDUsuario)

		JSON = {"idViaje": str(IDViaje),
			"datosPasajero": self._acondicionarJSONUsuario(datosUsuario), 
			"ruta": ruta["mongo"]["ruta"],
			"origen": ruta["mongo"]["origen"],
			"origenGrados": ruta["mongo"]["origenGrados"],
			"destino": ruta["mongo"]["destino"],
			"destinoGrados": ruta["mongo"]["destinoGrados"],
			"costo": str(cotizacion)}


		return JSON

	def _obtener_ID_viaje(self, IDUsuario):
		"""!@brief Obtiene el id del viaje a insertar usando el contador autoincremental de cada conductor."""

		conductores = mongo.db.conductores
		ID = conductores.find_and_modify({"id": IDUsuario}, {"$inc": {"contadorViajes": 1}}, upsert=True, new=True)

		return ID["contadorViajes"]
		

	def _acondicionarJSONUsuario(self, datos):
		"""!@brief Metodo intermedio para asegurar la normalizacion de la informacion."""
		datos = datos["user"]
		JSON = {"idPasajero": datos["id"],
			"nombreUsuario": datos["username"],
			"nombre": datos["name"],
			"apellido": datos["surname"],
			"pais": datos["country"],
			"email": datos["email"],
			"fechaNacimiento": datos["birthdate"],
			"imagenes": datos["images"]}

		return JSON

	def _guardar_viaje_mongo(self, datos):
		conductores = mongo.db.conductores
		usuarios = mongo.db.usuarios
		res = None
		
		try:
			res = conductores.update({"id" : self.IDUsuario, "estado": "libre"}, {"$push": {"viajes" : datos}})
			if(res["nModified"] == 0):
				return False

		except Exception as e:
			return False
		return True

	def _acondicionarJSONRuta(self, datos):
		"""!@brief Acondiciona la salida de Google Directions.

		@param datos Es lo que devuelva Google Directions."""


		json = {}

		dato = datos["routes"][0]["legs"][0]["steps"]
		
		i = 0
		for prop in dato:
			json[str(i)] = {"inicio": prop["start_location"], "fin": prop["end_location"]}
			i = i + 1

		"""Convierte a metros"""
		origenJSON = {"lng": vincenty((0,float(datos["routes"][0]["legs"][0]["start_location"]["lng"])), origen).meters,
			  "lat": vincenty((float(datos["routes"][0]["legs"][0]["start_location"]["lat"]),0), origen).meters}

		destinoJSON = {"lng": vincenty((0,float(datos["routes"][0]["legs"][0]["end_location"]["lng"])), origen).meters,
			  "lat": vincenty((float(datos["routes"][0]["legs"][0]["end_location"]["lat"]),0), origen).meters}

		JSON = {"origen": datos["routes"][0]["legs"][0]["start_location"],
			"destino": datos["routes"][0]["legs"][0]["end_location"],
				"mongo": {"ruta": {"ruta": json, "distancia": datos["routes"][0]["legs"][0]["distance"]["value"]},
					  "distancia": datos["routes"][0]["legs"][0]["distance"]["value"],
					  "origen": origenJSON,
					  "destino": destinoJSON,
					  "origenGrados": datos["routes"][0]["legs"][0]["start_location"],
					  "destinoGrados": datos["routes"][0]["legs"][0]["end_location"]}
			}

		return JSON

	def _obtener_ruta_directions(self, origen, destino):
		"""!@brief Realiza la peticion a Google Directions."""


		parametros = {"origin": origen,
			      "destination": destino,
			      "key": directionsAPIKey};

		self.conectividad.setURL(URLGoogleDirections)
		return self.conectividad.get("json", parametros)

	def _calcular_ruta(self, origen, destino):
		"""!@Brief Pide el servicio a Google Directions."""

		datos = self._obtener_ruta_directions(origen, destino)
		if(not datos):
			return False

		"""Devuelve el JSON acondicionado.""" 
		datos = self._acondicionarJSONRuta(datos)
		return datos

	def _informar_viaje(self, IDUsuario):
		"""!@Brief Envia la notificacion push al conductor para avisarle que puede aceptar un viaje."""

		URLPUSH = "https://fcm.googleapis.com/fcm"
		self.conectividad.setURL(URLPUSH)
		headers = {"content-type": "application/json",
			   "Authorization": "key=AAAAIqy7cgs:APA91bFJ1BC7rlvrQKoQNcpubZqxg_jVy1rgSH0pWxGC6Z_yN_RUAmyduc5S9j2xcC7UeLT5fy2L9bm2HGtvzYhn7daWFJgalLBxtz7ID73KprwZhQXBmZcEd05d7k_cXftN_YVifStn"}
		
		parametros = {}
		cuerpo = {"to":	"/topics/"+IDUsuario,
			  "notification": {"title": "Nuevo viaje disponible",
					   "text": "Tenes un nuevo viaje para aceptar!"
					  }		
			 }
		
		self.conectividad.post("send", cuerpo, parametros, headers)

		return True
	


