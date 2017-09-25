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

class Auth(Resource):
	"""!@brief Clase para autenticacion y creacion del Token. 
	"""

	autenticador = Token() 

	def __init__(self):
		app = Flask(__name__)

	def post(self):
		"""!@brief Autentica al usuario una unica vez."""
		response = None
		try:
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Request no tiene un json")

			"""Si no se recibieron los datos todo mal."""
			nombreUsuario = self._get_user_from_request()
			contrasena = self._get_hashPassword_from_request()

			if(not nombreUsuario or not contrasena):
				return ErrorHandler.create_error_response(500, "No se recibieron los campos esperados del json.")

			"""Primero verifica que exista en el shared server."""
			if(not self._existe_usuario_en_sharedServer(nombreUsuario, contrasena)):
				return ErrorHandler.create_error_response(404, "No existe usuario registrado con esas credenciales.")

			token = Auth.autenticador.obtenerToken(nombreUsuario, contrasena)
			
			if(not token):
				return ErrorHandler.create_error_response(500, "No se pudo generar el token.")

			jsonToken = {}
			jsonToken['token'] = token
			response = ResponseBuilder.build_response(jsonToken, '200')

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response

	def _get_user_from_request(self):
		"""!@brief Obtiene el nombre de usuario de la request. 
			"""
		return request.get_json()["nombreUsuario"]
	
	def _get_hashPassword_from_request(self):
		"""!@brief Obtiene la contraseña de la request. 
			"""
		return request.get_json()["contrasena"]

	def _validate_request(self):
		"""!@brief Valida que haya una request. 
			"""
		datos = request.get_json(silent=True);

		if(not datos):
			return False
		else:
			return True
	def _existe_usuario_en_sharedServer(self, nombreUsuario, contrasena):
		return True
