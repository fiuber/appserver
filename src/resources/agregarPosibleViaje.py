# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token
from src.models.conectividad import Conectividad

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo
from src import directionsAPIKey

class AgregarPosibleViaje(Resource):
	"""!@brief Clase para agregar un viaje a la lista de posibles viajes de un chofer."""


	def __init__(self):
		self.URLDirections = "https://maps.googleapis.com/maps/api/directions"
		self.URL = "http://fiuber-shared.herokuapp.com"
		self.autenticador = Token() 
		self.conectividad = Conectividad(self.URL)

	def post(self, IDUsuario):
		"""!@brief Agrega la informacion del viaje posible."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el JSON con los datos del auto."""
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")
			self.IDUsuario = IDUsuario

			"""Guarda el posible viaje en mongoDB."""
			datos = self._obtenerJSONViaje()
			if(not self._guardar_viaje_mongo(datos)):
				return ErrorHandler.create_error_response(404, "Imposible guardar datos de viaje.")

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

	def _obtenerJSONViaje(self):
		"""!@brief Obtiene toda la informacion y crea el JSON de datos del viaje."""

		"""Pide la informacion del usuario al Shared Server."""
		datosUsuario = self.conectividad.get("users/"+self._get_data_from_request("IDPasajero"))
		if(not datosUsuario):
			return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")
		
		"""Pide la cotizacion del viaje al Shared Server."""
		datosCotizacion = "13"
		if(not datosCotizacion):
			return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

		"""Obtiene el ID de viaje a insertar"""
		
		IDViaje = self._obtener_ID_viaje(self.IDUsuario)

		JSON = {"idViaje": IDViaje,
			"datosPasajero": self._acondicionarJSONUsuario(datosUsuario), 
			"ruta": self._calcular_ruta(self._get_data_from_request("origen"), self._get_data_from_request("destino")),
			"costo": datosCotizacion}

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
		res = None
		
		try:
			res = conductores.update({"id" : self.IDUsuario}, {"$push": {"viajes" : datos}}, upsert=True)
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
		

		return {"ruta": json}

	def _obtener_ruta_directions(self, origen, destino):
		"""!@brief Realiza la peticion a Google Directions."""


		parametros = {"origin": origen,
			      "destination": destino,
			      "key": directionsAPIKey};

		self.conectividad.setURL(self.URLDirections)
		return self.conectividad.get("json", parametros)

	def _calcular_ruta(self, origen, destino):
		"""!@Brief Pide el servicio a Google Directions."""

		datos = self._obtener_ruta_directions(origen, destino)
		if(not datos):
			return ErrorHandler.create_error_response(404, "Imposible obtener ruta.")

		"""Devuelve el JSON acondicionado.""" 
		datos = self._acondicionarJSONRuta(datos)
		return datos

