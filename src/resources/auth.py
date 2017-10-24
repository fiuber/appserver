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

class Auth(Resource):
	"""!@brief Clase para autenticacion y creacion del Token."""

	def __init__(self):
		self.conectividad = Conectividad("http://fiuber-shared.herokuapp.com")
		self.autenticador = Token() 

	def post(self):
		"""!@brief Autentica al usuario una unica vez."""
		response = None
		
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

		token = self.autenticador.obtenerToken(self.id, self.tipo, nombreUsuario, contrasena)
		
		if(not token):
			return ErrorHandler.create_error_response(500, "No se pudo generar el token.")

		jsonToken = {}
		jsonToken['token'] = token
		jsonToken["id"] = self.id
		jsonToken["tipo"] = self.tipo

		response = ResponseBuilder.build_response(jsonToken, '200')

		
		return response

	def _get_user_from_request(self):
		"""!@brief Obtiene el nombre de usuario de la request."""
		datos = None;
		try:
			datos = request.get_json()["nombreUsuario"]
		except Exception as e:
			datos = False
		return datos
	
	def _get_hashPassword_from_request(self):
		"""!@brief Obtiene la contraseña de la request.	""" 
		datos = None;
		try:
			datos = request.get_json()["contrasena"]
		except Exception as e:
			datos = False
		return datos

	def _validate_request(self):
		"""!@brief Valida que haya una request."""

		
		if(request.get_json() == None):
			return False
		else:
			return True
	
	def _existe_usuario_en_sharedServer(self, nombreUsuario, contrasena):
		"""!@brief Valida al usuario con el shared server."""

		cuerpo = {'username': nombreUsuario, 'password': contrasena}

		respuesta = self.conectividad.post("users/validate", cuerpo)

		if(respuesta != False):
			self.id = respuesta["user"]["id"]
			self.tipo = respuesta["user"]["type"]

		return respuesta != False
