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

class ModificarMetodoPago(Resource):
	"""!@brief Clase para actualizar los metodos de pago del usuario."""


	def __init__(self):
		self.autenticador = Token() 

	def put(self, IDUsuario):
		"""!@brief Actualizar los metodos de pago del usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el JSON con los datos del metodo de pago."""
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(404, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Actualiza el metodo de pago dado si es valido."""

		
			if(not self._actualizar_metodopago_usuario(IDUsuario)):
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

		res = self._get_data_from_request("metodo") and self._get_data_from_request("parametros")

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

	def _actualizar_metodopago_usuario(self, IDUsuario):
		"""!@brief Actualiza el metodo de pago a mongoDB."""
		 
		usuario = mongo.db.usuarios.find_one({"id" : IDUsuario})
		if(not usuario):
			return False

		JSON = self._acondicionarJSON()
		if(not JSON):
			return False

		haySeleccion = False
		try:
			haySeleccion = self._get_data_from_request("seleccionado")
		except Exception as e:
			haySeleccion = False

		JSONSet = {"$set": {"metodopago"+"."+self._get_data_from_request("metodo"): JSON}}

		"""Se selecciona el metodo si asi lo especifico la peticion en el campo 'seleccionado' o  no hay otro"""
		if(haySeleccion or usuario.get("metodopago",{}).get("seleccionado", None) == None):
			JSONSet["$set"]["metodopago.seleccionado"] = self._get_data_from_request("metodo")

		mongo.db.usuarios.update({"id" : IDUsuario}, JSONSet)

		return True


	def _acondicionarJSON(self):
		"""!@brief Normaliza los datos en JSON."""

		JSONParametros = None
		try:
			if(self._get_data_from_request("metodo") == "efectivo"):
				JSONParametros = {"moneda": self._get_data_from_request("parametros")["moneda"]}
			elif(self._get_data_from_request("metodo") == "tarjeta"):
				JSONParametros = {"moneda": self._get_data_from_request("parametros")["moneda"],
						  "numero": self._get_data_from_request("parametros")["numero"],
						  "fechaVencimiento": self._get_data_from_request("parametros")["fechaVencimiento"],
						  "cvv": self._get_data_from_request("parametros")["cvv"]}
			else:
				return False
		
			JSONParametros

		except Exception as e:
			return False

		return JSONParametros



