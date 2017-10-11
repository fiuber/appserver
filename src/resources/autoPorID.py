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

class AutoPorID(Resource):
	"""!@brief Clase para la busqueda de un auto de un conductor."""

	def __init__(self):
		app = Flask(__name__)
		self.URL = "http://fiuberappserver.herokuapp.com"
		self.TOKEN = "uidsfdsfuidsfjkdfsjhi" 
		self.autenticador = Token() 
		self.conectividad = Conectividad(self.URL, self.TOKEN)	

	def get(self, IDUsuario, IDAuto):
		"""!@brief Obtiene los datos de un auto de un conductor."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le pide los datos al Shared Server."""
			URLDestino = "users/"+IDUsuario+"/cars/"+IDAuto
			datos = self.conectividad.get(URLDestino)
			if(not datos):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

			"""Devuelve el JSON acondicionado.""" 
			datos = self._acondicionarJSON(datos)
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

	def _acondicionarJSON(self, datos):
		"""!@brief Acondiciona un solo auto pasado.

		@param datos Es el auto a acondicionar."""

		return {"modelo": datos["modelo"],
			"color": datos["color"],
			"patente": datos["patente"],
			"anio": datos["anio"],
			"estado": datos["estado"],
			"aireAcondicionado": datos["aireAcondicionado"],
			"musica": datos["musica"]}
		
