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
from src import app
from src import URLSharedServer
from src import mongo

class AgregarAutoUsuario(Resource):
	"""!@brief Clase para agregar un auto a un usuario."""


	def __init__(self):
		self.autenticador = Token() 
		self.conectividad = Conectividad(URLSharedServer)	

	def post(self, IDUsuario):
		"""!@brief Asocia informacion de un nuevo auto a un usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el JSON con los datos del auto."""
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le manda los datos al Shared Server y guarda en mongoDB."""
			self.conectividad.setURL(URLSharedServer)
			res = self.conectividad.post("users/"+IDUsuario+"/cars", self._obtenerJSONPropiedadesAuto())
			if(not res):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")
			else:
				dato = mongo.db.conductores.find_and_modify({"id": IDUsuario},{"$push": {"autosRegistrados": res["car"]["id"]}}, new = True)
				if(not dato.get("autoActivo",{}) or self._get_data_from_request("activo") == True):
					mongo.db.conductores.update({"id": IDUsuario},{"$set": {"autoActivo": res["car"]["id"]}})				
			

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response

	def _get_data_from_request(self, nombrePropiedad, defecto = False):
		"""!@brief Obtiene la propiedad del json contenido de la request."""
		
		try:
			return request.get_json()[nombrePropiedad]
		except Exception as e:
			return defecto

	def _validate_request(self):
		"""!@brief Valida que haya una request completa (se fija solo algun parametro)."""

		res = self._get_data_from_request("modelo")

		if(not res):
			return False
		else:
			return True

	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = self.autenticador.validarToken(token)
		if(not res):
			return False
		return True

	def _obtenerJSONPropiedadesAuto(self):
		return {"id": "null", "_ref": "null", "owner": "null", 
			"properties":  
				[{"name" : "modelo", "value" : self._get_data_from_request("modelo")},
				{"name" : "color", "value" : self._get_data_from_request("color")},
				{"name" : "patente", "value" : self._get_data_from_request("patente")},
				{"name" : "anio", "value" : self._get_data_from_request("anio")},
				{"name" : "estado", "value" : self._get_data_from_request("estado")},
				{"name" : "aireAcondicionado", "value" : self._get_data_from_request("aireAcondicionado")},
				{"name" : "musica", "value" : self._get_data_from_request("musica")},
				{"name" : "imagen", "value" : self._get_data_from_request("imagen", None)}]
					
			}

