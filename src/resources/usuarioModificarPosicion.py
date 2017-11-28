# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token
from geopy.distance import vincenty

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo
from src import origen

class UsuarioModificarPosicion(Resource):
	"""!@brief Clase para actualizar la posicion de un usuario."""


	def __init__(self):
		self.autenticador = Token() 

	def put(self, IDUsuario):
		"""!@brief Actualiza los datos de posicion de un usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el JSON con los datos de la posicion."""
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Actualiza la posicion."""
			pos = self._get_data_from_request("posicion")

		
			if(not self._actualizar_posicion_usuario(IDUsuario, pos["lng"], pos["lat"])):
				return ErrorHandler.create_error_response(500, "No se pudo actualizar la posicion.")

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

		res = self._get_data_from_request("posicion")

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

	def _actualizar_posicion_usuario(self, IDUsuario, x, y):
		
		"""Convierte a metros"""

		x = vincenty((0,x), origen).meters
		y = vincenty((y,0), origen).meters

		return mongo.db.usuarios.update({"id" : IDUsuario}, {"$set": {"posicion" : {"lng": x, "lat": y}}}, upsert=True)
		
