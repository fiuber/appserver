# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo

class EliminarMetodoPago(Resource):
	"""!@brief Clase para eliminar los metodos de pago del usuario."""


	def __init__(self):
		self.autenticador = Token() 

	def delete(self, IDUsuario):
		"""!@brief Eliminar los metodos de pago del usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el JSON con los datos del metodo de pago."""
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(404, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Borrar el metodo de pago si es valido."""

			if(not self._eliminar_metodopago_usuario(IDUsuario)):
				return ErrorHandler.create_error_response(500, "Metodo de pago no valido.")

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

		res = self._get_data_from_request("metodo")

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

	def _eliminar_metodopago_usuario(self, IDUsuario):
		"""!@brief Elimina el metodo de pago de mongoDB."""
		
		usuarios = mongo.db.usuarios
		usuario = usuarios.find_one({"id" : IDUsuario})
		if(not usuario):
			return False

		JSONSet = {}

		if(self._get_data_from_request("metodo") == "efectivo"):
			JSONSet = {"$unset": {"metodopago.efectivo": ""}}
			if("tarjeta" in usuario["metodopago"]):
				JSONSet["$set"] = {"metodopago.seleccionado": "tarjeta"}
			else:
				JSONSet["$set"] = {"metodopago.seleccionado": None}
		
		elif(self._get_data_from_request("metodo") == "tarjeta"):
			JSONSet = {"$unset": {"metodopago.tarjeta": ""}}
			if("efectivo" in usuario["metodopago"]):
				JSONSet["$set"] = {"metodopago.seleccionado": "efectivo"}
			else:
				JSONSet["$set"] = {"metodopago.seleccionado": None}
		else:
			return False

		usuarios.update({"id" : IDUsuario},JSONSet)



		return True


