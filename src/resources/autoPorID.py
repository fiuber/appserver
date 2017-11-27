# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token
from src.models.conectividad import *

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import URLSharedServer
from src import mongo

class AutoPorID(Resource):
	"""!@brief Clase para la busqueda de un auto de un conductor."""

	def __init__(self):
		self.autenticador = Token() 

	def get(self, IDUsuario, IDAuto):
		"""!@brief Obtiene los datos de un auto de un conductor."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le pide los datos al Shared Server."""
			URLDestino = "users/"+IDUsuario+"/cars/"+IDAuto
			datos = conectividad.get(URLSharedServer, URLDestino)
			if(not datos):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

			"""Devuelve el JSON acondicionado.""" 
			datos = self._acondicionarJSON(datos, IDUsuario)
			if(not datos):
				response = ErrorHandler.create_error_response(500, "No existe el conductor.")
			response = ResponseBuilder.build_response(datos, '200')

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response


	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = self.autenticador.validarToken(token)
		if(not res):
			return False
		return True

	def _acondicionarJSON(self, datos, IDUsuario):
		"""!@brief Acondiciona un solo auto pasado.

		@param datos Es el auto a acondicionar."""

		json = {}

		dato = datos["car"]["properties"]
		json["_ref"] = datos["car"]["_ref"]
		json["id"] = datos["car"]["id"]

		conductor = mongo.db.conductores.find_one({"id": IDUsuario})
		if(not conductor):
			return False
		

		json["autoActivo"] = (json["id"] == conductor.get("autoActivo",False))

		for prop in dato:
			json[prop["name"]] = prop["value"]
		

		return json
