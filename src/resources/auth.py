# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token
from src.resources import conectividad

from error_handler import ErrorHandler
from response_builder import ResponseBuilder

from src import URLSharedServer
from src import URLFacebook
from src import mongo

class Auth(Resource):
	"""!@brief Clase para autenticacion y creacion del Token."""

	def __init__(self):
		self.autenticador = Token()

	def post(self):
		"""!@brief Autentica al usuario una unica vez."""

		respuesta = None

		"""Si es con facebook sigue otro camino"""
		if(self._get_data_from_request("tokenFacebook")):
			respuesta = self.autenticarConFacebook()
		else:
			respuesta = self.autenticarConDatos()

		return respuesta


	def autenticarConFacebook(self):
		"""!@brief Autentica usando el token de facebook."""

		response = None
		
		valid = self._validate_request()
		if(not valid):
			return ErrorHandler.create_error_response(500, "Request no tiene un json")

		tokenFacebook = self._get_data_from_request("tokenFacebook")
		idFacebook = self._obtenerIDFacebook(tokenFacebook)
		if(not idFacebook):
			return ErrorHandler.create_error_response(404, "Token de facebook erroneo.")

		"""Si es cuenta usando facebook el usuario y contrasena es autogenerada y esta en mongoDB"""
		usuario = None
		usuario = mongo.db.usuarios.find_one({"idFacebook": idFacebook})
		if(not usuario):
			usuario = mongo.db.conductores.find_one({"idFacebook": idFacebook})
			if(not usuario):
				return ErrorHandler.create_error_response(404, "No existe usuario registrado con esas credenciales.")
		

		"""Primero verifica que exista en el shared server."""
		if(not self._existe_usuario_en_sharedServer(usuario["nombreUsuario"], usuario["contrasena"])):
			return ErrorHandler.create_error_response(404, "No existe usuario registrado con esas credenciales.")

		token = self.autenticador.obtenerToken(self.id, self.tipo, usuario["nombreUsuario"], usuario["contrasena"])
		
		if(not token):
			return ErrorHandler.create_error_response(500, "No se pudo generar el token.")

		jsonToken = {}
		jsonToken['token'] = token
		jsonToken["id"] = self.id
		jsonToken["tipo"] = self.tipo

		if(self.tipo == "driver"):
			self._guardar_autos_mongo(self.respuesta["user"]["cars"], self.respuesta["user"]["id"])

		response = ResponseBuilder.build_response(jsonToken, '200')

		
		return response

	def autenticarConDatos(self):
		"""!@brief Autentica usando usuario y contrasena."""

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

		if(self.tipo == "driver"):
			self._guardar_autos_mongo(self.respuesta["user"]["cars"], self.respuesta["user"]["id"])

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
		"""!@brief Obtiene la contrasena de la request.	""" 
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

		respuesta = conectividad.post(URLSharedServer, "users/validate", cuerpo)

		self.respuesta = respuesta

		if(respuesta != False):
			self.id = respuesta["user"]["id"]
			self.tipo = respuesta["user"]["type"]

		return respuesta != False

	def _guardar_autos_mongo(self, autos, IDUsuario):
		"""!@brief Guarda los id de los auto en mongoDB para futura referencia."""
		
		arregloIDS = []

		for x in autos:
			arregloIDS.append(x["id"])

		if(len(arregloIDS)):
			mongo.db.conductores.update({"id": IDUsuario}, {"$set": {"autosRegistrados": arregloIDS}}, upsert=True)

	
	def _get_data_from_request(self, nombrePropiedad):
		"""!@brief Obtiene la propiedad del json contenido de la request."""
		
		try:
			return request.get_json()[nombrePropiedad]
		except Exception as e:
			return False

	def _obtenerIDFacebook(self, tokenFacebook):		
		"""!@brief Pide a la URL de la API de facebook el id asociado al token."""

		res = conectividad.get(URLFacebook,"me",{"access_token": tokenFacebook})
		if(not res):	
			return False

		return res["id"]
			
	
