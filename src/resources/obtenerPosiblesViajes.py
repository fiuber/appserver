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

class ObtenerPosiblesViajes(Resource):
	"""!@brief Clase para obtener la lista de posibles viajes de un chofer."""


	def __init__(self):
		self.autenticador = Token() 

	def get(self, IDUsuario):
		"""!@brief Obtiene la informacion de todos los viajes posibles."""
		response = ResponseBuilder.build_response({}, '200')
	

		"""Primero valida el token."""
		if(not self._validar_token()):
			return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

		"""Devuelve los posibles viajes."""
		try:
			datos = self._obtenerJSONViajes(IDUsuario)
			response = ResponseBuilder.build_response(datos, '200')
		except Exception as e:
			mongo.db.log.insert({"Tipo": "Error", "Mensaje": "1 - "+str(e)})
			response = ErrorHandler.create_error_response(400, "No existe el conductor.")

		return response

	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = self.autenticador.validarToken(token)
		if(not res):
			return False
		return True

	def _obtenerJSONViajes(self, IDUsuario):
		"""!@brief Obtiene toda la informacion y crea el JSON de datos del viajes."""
		
		conductores = mongo.db.conductores
		conductor = conductores.find_one({"id": IDUsuario})
		
		if(not conductor.get("id", False)):
			mongo.db.log.insert({"Tipo": "Error", "Mensaje": "2 - No existe el "+str(IDUsuario)+" - "+str(conductor)})
			raise Exception("No existe el conductor.")

		if(not conductor.get("viajes",False)):
			return {}

		JSON = {}

		i = 0

		for prop in conductor["viajes"]:
			JSON[str(i)] = prop
			i = i + 1
		
		return JSON

