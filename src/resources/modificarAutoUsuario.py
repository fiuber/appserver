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

class ModificarAutoUsuario(Resource):
	"""!@brief Clase para modificar un auto de un usuario."""


	def __init__(self):
		self.URL = "http://fiuber-shared.herokuapp.com"
		self.autenticador = Token() 
		self.conectividad = Conectividad(self.URL)	


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
			res = self.conectividad.put(URLDestino, self._obtenerJSON(IDUsuario, IDAuto))
			
			if(not res):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")
			response = ResponseBuilder.build_response({"_ref": res["car"]["_ref"]}, '200')

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
		return [{"name" : "modelo", "value" : self._get_data_from_request("modelo")},
				{"name" : "color", "value" : self._get_data_from_request("color")},
				{"name" : "patente", "value" : self._get_data_from_request("patente")},
				{"name" : "anio", "value" : self._get_data_from_request("anio")},
				{"name" : "estado", "value" : self._get_data_from_request("estado")},
				{"name" : "aireAcondicionado", "value" : self._get_data_from_request("aireAcondicionado")},
				{"name" : "musica", "value" : self._get_data_from_request("musica")}]

	def _obtenerJSON(self, IDUsuario, IDAuto):
		return {"id": IDAuto,
			"_ref": self._get_data_from_request("_ref"),
			"owner": IDUsuario,
			"properties": self._obtenerJSONPropiedadesAuto()}

		
