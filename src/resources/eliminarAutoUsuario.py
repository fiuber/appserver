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
from src import app
from src import URLSharedServer
from src import mongo

class EliminarAutoUsuario(Resource):
	"""!@brief Clase para eliminar un auto de un usuario."""



	def __init__(self):
		self.autenticador = Token() 

	def delete(self, IDUsuario, IDAuto):
		"""!@brief Elimina un auto de un usuario determinado."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Le manda los datos al Shared Server."""
			URLDestino = "users/"+IDUsuario+"/cars/"+IDAuto
			if(not conectividad.delete(URLSharedServer, URLDestino)):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con Shared Server")

			"""Actualizo la informacion en mongoDB."""
			res = mongo.db.conductores.find_and_modify({"id": IDUsuario},{"$pull": {"autosRegistrados": IDAuto}}, new=True)
			if(not res):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con MongoDB")
			
			"""Si ese auto era el seleccionado se pone otro o se borra el campo."""
			if(res["autoActivo"] == IDAuto and len(res.get("autosRegistrados", []))):
				res = mongo.db.conductores.update({"id": IDUsuario},{"$set": {"autoActivo": res["autosRegistrados"][0]}})
				if(res["nModified"] == 0):
					return ErrorHandler.create_error_response(404, "Imposible comunicarse con MongoDB")
			elif(len(res.get("autosRegistrados", [])) == 0):
				res = mongo.db.conductores.update({"id": IDUsuario},{"$unset": {"autoActivo": ""}})
				if(res["nModified"] == 0):
					return ErrorHandler.create_error_response(404, "Imposible comunicarse con MongoDB")

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

