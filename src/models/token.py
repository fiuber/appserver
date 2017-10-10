# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo

class Token(Resource):
	"""!@brief Clase para autenticacion y creacion del Token."""

	def __init__(self):
		app = Flask(__name__)
		app.config['MONGO_DBNAME'] = 'fiuberappserver'
		app.config['MONGO_URI'] = 'mongodb://fiuberappserver:fiuberappserver@ds123534.mlab.com:23534/fiuberappserver'
		self.mongo = PyMongo(app)
		self.CLAVE_ULTRASECRETA = "SV3v9%\"$:G0:E?."

	def obtenerToken(self, nombreUsuario, contrasena):
		"""!@brief Autentica al usuario una unica vez. Si el usuario no tenia un token anterior o expiro se crea uno y se almacena, sino se devuelve el que ya tenia asignado."""
		try:
			token = self._recuperarToken(nombreUsuario)
			valido = self._validarToken(nombreUsuario, contrasena, token)
		
			"""Si no estaba el token o no es valido se crea otro"""
			if(not token or not valido):
				token = self._crear_token(nombreUsuario, contrasena)
			return token

		except Exception as e:
			return False

	def _validarToken(self, token, nombreUsuario):
		token = self._recuperarToken(nombreUsuario)
		valido = self._validarTokenLogin(nombreUsuario, contrasena, token)
		return token and valido

	def _crear_token(self, nombreUsuario, contrasena):
		""""Se crea un nuevo token."""		
		token = self._generarToken(nombreUsuario, contrasena)
		if(not token):
			return False

		"""Si no se puede almacenar no tiene sentido seguir aunque el token se haya generado"""
		if(not self._almacenarToken(nombreUsuario, token)):
			return False

		return token

	def _recuperarToken(self, nombreUsuario):
		"""!@brief Recupera el token de mongoDB. 
		Devuelve el token o false.
		
		@param nombreUsuario Nombre del usuario."""

		try:
			usuarios = self.mongo.db.usuarios
			usuario = usuarios.find_one({'nombreUsuario': nombreUsuario})
			if(usuario):
				return usuario['token']
			else:
				return False
		except Exception as e:
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
		@param token token a guardar."""

		usuarios = self.mongo.db.usuarios
		
		usuarios.update_one({"nombreUsuario" : nombreUsuario}, {"token": token}, upsert=True)
		return True
	

	def _validarTokenLogin(self, nombreUsuario, contrasena, token):
		"""!@brief Desempaqueta el token y valida los campos.
		Devuelve true o false.
		
		@param nombreUsuario Nombre del usuario.
		@param contrasena Contrasena del usuario hasheada.
		@param token token a validar."""

		try:
			payload = jwt.decode(token, CLAVE_ULTRASECRETA)
			if(payload['nombreUsuario'] == nombreUsuario and payload['contrasena'] == contrasena):
				return True;
			else:
				return False;

		except Exception as e:
			return False

	def validarToken(self, token):
		"""!@brief Valida el token.
		
		@param token Token a validar."""

		try:
			payload = jwt.decode(token, self.CLAVE_ULTRASECRETA)
			return True

		except Exception as e:
			return False

		
