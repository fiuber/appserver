# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo

from error_handler import ErrorHandler
from response_builder import ResponseBuilder

class Token(Resource):
	"""!@brief Clase para autenticacion y creacion del Token. 
	"""

	def __init__(self):
		app = Flask(__name__)
		app.config['MONGO_DBNAME'] = 'fiuberappserver'
		app.config['MONGO_URI'] = 'mongodb://fiuberappserver:fiuberappserver@ds123534.mlab.com:23534/fiuberappserver'
		self.mongo = PyMongo(app)
		self.CLAVE_ULTRASECRETA = "SV3v9%\"$:G0:E?."

	def post(self):
		"""!@brief Autentica al usuario una unica vez."""
		response = None
		try:
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(404, "Request no tiene un json")

			"""Si no se recibieron los datos todo mal."""
			nombreUsuario = self._get_user_from_request()
			contrasena = self._get_hashPassword_from_request()

			if(not nombreUsuario or not contrasena):
				return ErrorHandler.create_error_response(404, "No se recibieron los campos esperados del json.")

			token = self._recuperarToken(nombreUsuario);

			"""Si no esta el token puede ser que no este autenticado todavia."""
			if(not token):
				"""
					Pegarle al server para ver si existe el usuario y si existe crearle un token y agregarlo
				"""
				existe = True;

				if(not existe):
					return ErrorHandler.create_error_response(404, "Usuario no registrado.")
			
				token = self._generarToken(nombreUsuario, contrasena)
				if(not token):
					return ErrorHandler.create_error_response(404, "Error al generar token.")

				"""Si no se puede almacenar no tiene sentido seguir aunque el token se haya generado"""
				if(not self._almacenarToken(nombreUsuario, token)):
					return ErrorHandler.create_error_response(404, "No se pudo acceder a mongoDB o el usuario no existe")

				jsonToken = {}
				jsonToken['token'] = token

				return json.dumps(jsonToken)
			
			"""Si es valido se le envia y sino error."""
			autentico = self._validarToken(nombreUsuario, contrasena, token)
			if(not autentico):
				return ErrorHandler.create_error_response(404, "Cagaste 6")

			response = ResponseBuilder.build_response(token, '200')

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

	def _recuperarToken(self, nombreUsuario):
		"""!@brief Recupera el token de mongoDB. 
		Devuelve el token o false.
		
		@param nombreUsuario Nombre del usuario.
		"""

		usuarios = self.mongo.db.usuarios
		usuario = usuarios.find_one({'nombreUsuario': nombreUsuario})
		if(usuario):
			usuario['token']
		else:
			return False

	def _generarToken(self, nombreUsuario, contrasena):
		"""!@brief Genera y devuelve el token de autenticacion del usuario con el appserver
		@param nombreUsuario Nombre del usuario.
		@param contrasena Contrasena del usuario hasheada.
		"""
		try:

			"""
			En el payload estan los datos propiamente dichos		
			"""
			payload = {
			    'exp': datetime.datetime.utcnow() + datetime.timedelta(days = 1),
			    'iat': datetime.datetime.utcnow(),
			    'nombreUsuario': nombreUsuario,
			    'contrasena': contrasena
			}
			return jwt.encode(
			    payload,
			    self.CLAVE_ULTRASECRETA,
			    algorithm = 'HS256'
			)
		except Exception as e:
			return False

	def _almacenarToken(self, nombreUsuario, token):
		"""!@brief Guarda el token en mongoDB para accederlo de una. 
		Devuelve true si se pudo guardar o false si no se pudo porque no existia el usuario
		
		@param nombreUsuario Nombre del usuario.
		@param token token a guardar.
		"""

		usuarios = self.mongo.db.usuarios
		
		usuarios.insert({"nombreUsuario" : nombreUsuario, "token": token})
		return True
	

	def _validarToken(self, nombreUsuario, contrasena, token):
		"""!@brief Desempaqueta el token y valida los campos.
		Devuelve true o false.
		
		@param nombreUsuario Nombre del usuario.
		@param contrasena Contrasena del usuario hasheada.
		@param token token a guardar.
		"""

		try:
			payload = jwt.decode(token, CLAVE_ULTRASECRETA)
			if(payload['nombreUsuario'] == nombreUsuario and payload['contrasena'] == contrasena):
				return True;
			else:
				return False;

		except jwt.ExpiredSignatureError:
			return False
		except jwt.InvalidTokenError:
			return False


		
