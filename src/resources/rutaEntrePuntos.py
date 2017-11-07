# -*- coding: utf-8 -*-
import jwt
import os
import datetime

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

class RutaEntrePuntos(Resource):
	"""!@brief Clase para la obtencion entre la ruta entre dos posiciones."""

	def __init__(self):
		self.URL = "https://maps.googleapis.com/maps/api/directions"
		self.autenticador = Token() 
		self.conectividad = Conectividad(self.URL)	

	def get(self):
		"""!@brief Obtiene la ruta entre dos posiciones."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el parametro origen y destino."""
			IDUsuario = self._validate_get_request()
			if(IDUsuario == False):
				return ErrorHandler.create_error_response(404, "Falta algun parametro.")

			"""Valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			datos = self._calcular_ruta(self._get_param_from_request("origen"), self._get_param_from_request("destino"))
			response = ResponseBuilder.build_response(datos, '200')

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response


	def _get_param_from_request(self, nombreParametro):
		"""!@brief Obtiene el parametro dado de la request."""
		return request.args.get(nombreParametro)


	def _validate_get_request(self):
		"""!@brief Tiene que estar la posicion origen y destino para hacer la busqueda."""
		datos = self._get_param_from_request("origen") and self._get_param_from_request("destino")

		if(not datos):
			return False
		else:
			return datos

	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = self.autenticador.validarToken(token)
		if(not res):
			return False
		return True

	def _acondicionarJSON(self, datos):
		"""!@brief Acondiciona la salida de Google Directions.

		@param datos Es lo que devuelva Google Directions."""


		json = {}

		dato = datos["routes"][0]["legs"][0]["steps"]
		
		i = 0
		for prop in dato:
			json[i] = {"inicio": prop["start_location"], "fin": prop["end_location"]}
			i = i + 1
		

		return {"ruta": json}

	def _obtener_ruta_directions(self, origen, destino):
		"""!@brief Realiza la peticion a Google Directions."""


		parametros = {"origin": origen,
			      "destination": destino,
			      "key": directionsAPIKey};

		return self.conectividad.get("json", parametros)

	def _calcular_ruta(self, origen, destino):
		"""!@Brief Pide el servicio a Google Directions."""

		datos = self._obtener_ruta_directions(origen, destino)
		if(not datos):
			return ErrorHandler.create_error_response(404, "Imposible obtener ruta.")

		"""Devuelve el JSON acondicionado.""" 
		datos = self._acondicionarJSON(datos)

		return datos
		

		
