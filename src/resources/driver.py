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

class Driver(Resource):
	"""!@brief Clase para el manejo de los datos de un conductor."""

	URL = "http://fiuberappserver.herokuapp.com"
	TOKEN = "uidsfdsfuidsfjkdfsjhi" 
	autenticador = Token() 
	conectividad = Conectividad(URL, TOKEN)	

	def __init__(self):
		app = Flask(__name__)

	def get(self):
		"""!@brief Obtiene los datos de un determinado conductor."""
		response = None
		try:
			valid = self._validate_get_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros de URL.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Pide al shared server los choferes cercanos al cliente."""

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response

	def post(self):
		"""!@brief Asocia informacion de un nuevo auto a un usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			valid = self._validate_post_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le manda los datos al Shared Server."""
			if(not conectividad.post("users/"+self._get_param_from_request("idUsuario")+"/cars", self._obtenerJSONPropiedadesAuto)))
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response

	def put(self):
		"""!@brief Modifica los datos de un auto de un determinado usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			valid = self._validate_put_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le manda los datos al Shared Server."""
			URLDestino = "users/"+self._get_param_from_request("idUsuario")+"/cars/"+self._get_param_from_request("idAuto")
			if(not conectividad.post(URLDestino, self.obtenerJSONPUT())))
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response

	def delete(self):
		"""!@brief Elimina un auto de un usuario determinado."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			valid = self._validate_delete_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le manda los datos al Shared Server."""
			URLDestino = "users/"+self._get_param_from_request("idUsuario")+"/cars/"+self._get_param_from_request("idAuto")
			if(not conectividad.delete(URLDestino))
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response


	def _get_data_from_request(self, nombrePropiedad):
		"""!@brief Obtiene la propiedad del json contenido de la request. 
			"""
		return request.get_json()["nombrePropiedad"]
	
	def _get_param_from_request(self, nombreParametro):
		"""!@brief Obtiene el parametro dado de la request."""
		return request.args.get(nombreParametro)

	def _validate_get_request(self):
		"""!@brief Valida que haya una request. 
			"""
		datos = request.get_json(silent=True);

		if(not datos):
			return False
		else:
			return True

	def _validate_post_request(self):
		"""!@brief Valida que haya una request completa."""

		res = self._get_param_from_request("idUsuario")
		res = res and self._get_data_from_request("modelo")

		if(not res):
			return False
		else:
			return True

	def _validate_put_request(self):
		"""!@brief Valida que haya una request completa."""

		res = self._get_param_from_request("idUsuario") and self._get_param_from_request("idAuto")
		res = res and self._get_data_from_request("modelo")

		if(not res):
			return False
		else:
			return True

	def _validate_delete_request(self):
		"""!@brief Valida que haya una request completa."""

		res = self._get_param_from_request("idUsuario") and self._get_param_from_request("idAuto")

		if(not res):
			return False
		else:
			return True

	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = autenticador.validarToken(token)
		if(!res)
			return False
		return True

	def _obtenerJSONPropiedadesAuto(self):
		return {"modelo": self._get_data_from_request("modelo"),
			"color": self._get_data_from_request("color"),
			"patente": self._get_data_from_request("patente"),
			"anio": self._get_data_from_request("anio"),
			"estado": self._get_data_from_request("estado"),
			"aireAcondicionado": self._get_data_from_request("aireAcondicionado"),
			"musica": self._get_data_from_request("musica")}

	def _obtenerJSONPUT(self):
		return {"id": self._get_param_from_request("idAuto") ,
			"_ref":,
			"owner": self._get_param_from_request("idUsuario"),
			"properties": self._obtenerJSONPropiedadesAuto()}

		
