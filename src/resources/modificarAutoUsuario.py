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

class ModificarAutoUsuario(Resource):
	"""!@brief Clase para modificar un auto de un usuario."""


	def __init__(self):
		app = Flask(__name__)
		self.URL = "http://fiuberappserver.herokuapp.com"
		self.TOKEN = "uidsfdsfuidsfjkdfsjhi" 
		self.autenticador = Token() 
		self.conectividad = Conectividad(self.URL, self.TOKEN)	


	def put(self, IDUsuario, IDAuto):
		"""!@brief Modifica los datos de un auto de un determinado usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el JSON con los datos del auto."""
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le manda los datos al Shared Server."""
			URLDestino = "users/"+IDUsuario+"/cars/"+IDAuto
			if(not self.conectividad.put(URLDestino, self._obtenerJSON(IDUsuario, IDAuto))):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

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

		res = self._get_data_from_request("modelo")

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

	def _obtenerJSONPropiedadesAuto(self):
		return {"modelo": self._get_data_from_request("modelo"),
			"color": self._get_data_from_request("color"),
			"patente": self._get_data_from_request("patente"),
			"anio": self._get_data_from_request("anio"),
			"estado": self._get_data_from_request("estado"),
			"aireAcondicionado": self._get_data_from_request("aireAcondicionado"),
			"musica": self._get_data_from_request("musica")}

	def _obtenerJSON(self, IDUsuario, IDAuto):
		return {"id": IDAuto,
			"_ref": "dsfjkfgjf",
			"owner": IDUsuario,
			"properties": self._obtenerJSONPropiedadesAuto()}

		