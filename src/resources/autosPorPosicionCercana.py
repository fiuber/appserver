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

class AutosPorPosicionCercana(Resource):
	"""!@brief Clase para la busqueda de autos de usuarios."""

	URL = "http://fiuberappserver.herokuapp.com"
	TOKEN = "uidsfdsfuidsfjkdfsjhi" 
	autenticador = Token() 
	conectividad = Conectividad(URL, TOKEN)	

	def __init__(self):
		app = Flask(__name__)

	def get(self):
		"""!@brief Obtiene los conductores cercanos a un determinado usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el parametro IDUsuario."""
			if(not self._validate_get_request):
				return ErrorHandler.create_error_response(404, "Falta el parametro IDUsuario.")

			"""Valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le pide los datos al Shared Server."""
			URLDestino = "users/"+IDUsuario+"/cars"
			datos = conectividad.get(URLDestino)
			if(not datos):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

			"""Devuelve el JSON acondicionado.""" 
			datos = _acondicionarJSON(datos)
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
		"""!@brief Tiene que estar el ID del usuario que realiza la busqueda."""
		datos = _get_param_from_request(self, "IDUsuario")

		if(not datos):
			return False
		else:
			return True

	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = autenticador.validarToken(token)
		if(not res):
			return False
		return True

	def _acondicionarAutoJSON(self, datos):
		"""!@brief Acondiciona un solo auto pasado.

		@param datos Es el auto a acondicionar."""

		return {"modelo": datos["modelo"],
			"color": datos["color"],
			"patente": datos["patente"],
			"anio": datos["anio"],
			"estado": datos["estado"],
			"aireAcondicionado": datos["aireAcondicionado"],
			"musica": datos["musica"]}

	def _acondicionarJSON(self, datos):
		"""!@brief Itera en los autos y arma el JSON.

		@param datos La response que se obtuvo del Shared Server."""


		json = {}
		i=0

		for auto in datos["cars"]:
			json[i] = _acondicionarAutoJSON(auto)
			i += 1

		return json

		
