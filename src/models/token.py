# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src import app
from src import mongo

class Token(Resource):
	"""!@brief Clase para autenticacion y creacion del Token."""

	def __init__(self):
		self.CLAVE_ULTRASECRETA = "SV3v9%\"$:G0:E?."

	def obtenerToken(self, IDUsuario, tipoUsuario, nombreUsuario, contrasena):
		"""!@brief Autentica al usuario una unica vez. Si el usuario no tenia un token anterior o expiro se crea uno y se almacena, sino se devuelve el que ya tenia asignado."""
		token = self._recuperarToken(nombreUsuario)
		valido = self._validarToken(nombreUsuario, contrasena, token)
		
		"""Si no estaba el token o no es valido se crea otro"""
		if(not token or not valido):
			token = self._crear_token(IDUsuario, tipoUsuario, nombreUsuario, contrasena)

		return token


	def _validarToken(self, nombreUsuario, contrasena, token):
		return self._validarTokenLogin(nombreUsuario, contrasena, token)

	def _crear_token(self, IDUsuario, tipoUsuario, nombreUsuario, contrasena):
		""""Se crea un nuevo token."""		
		token = self._generarToken(nombreUsuario, contrasena)
		if(not token):
			return False

		
		if(self._almacenarToken(IDUsuario, tipoUsuario, nombreUsuario, token) == False):
			return False
			
		return token

	def _recuperarToken(self, nombreUsuario):
		"""!@brief Recupera el token de mongoDB. 
		Devuelve el token o false.
		
		@param nombreUsuario Nombre del usuario."""

		try:
			usuarios = mongo.db.usuarios
			usuario = usuarios.find_one({'nombreUsuario': nombreUsuario})
			if(usuario):
				return usuario['token']

			conductores = mongo.db.conductores
			conductor = conductores.find_one({'nombreUsuario': nombreUsuario})
			if(conductor):
				return conductor['token']
			
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
			token = jwt.encode(
			    payload,
			    self.CLAVE_ULTRASECRETA,
			    algorithm = 'HS256')
			
			return token
			
		except Exception as e:
			return False

	def _almacenarToken(self, IDUsuario, tipoUsuario, nombreUsuario, token):
		"""!@brief Guarda el token en mongoDB para accederlo de una. 
		Devuelve true si se pudo guardar o false si no se pudo porque no existia el usuario
		
		@param nombreUsuario Nombre del usuario.
		@param token token a guardar."""

		try:
			if(tipoUsuario == "passenger"):
				base = mongo.db.usuarios
			else:
				base = mongo.db.conductores

			base.update({"id" : IDUsuario}, {"id": IDUsuario,"nombreUsuario" : nombreUsuario, "token": token}, upsert=True)


		except Exception as e:
			return False

		return True
	

	def _validarTokenLogin(self, nombreUsuario, contrasena, token):
		"""!@brief Desempaqueta el token y valida los campos.
		Devuelve true o false.
		
		@param nombreUsuario Nombre del usuario.
		@param contrasena Contrasena del usuario hasheada.
		@param token token a validar."""

		try:
			payload = jwt.decode(token, self.CLAVE_ULTRASECRETA)
			if(payload['nombreUsuario'] == nombreUsuario and payload['contrasena'] == contrasena):
				return True
			else:
				return False

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

		
