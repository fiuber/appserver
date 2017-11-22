# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import time
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token
from src.models.push import enviarNotificacionPush
from src.models.conectividad import Conectividad

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo
from src import URLSharedServer

class RechazarViaje(Resource):
	"""!@brief Clase para rechazar un viaje."""


	def __init__(self):
		self.autenticador = Token() 

	def delete(self, IDUsuario, IDViaje):
		"""!@brief Rechaza un viaje."""
		response = ResponseBuilder.build_response({}, '200')
		try:

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Devuelve los posibles viajes."""
			datos = self._quitar_viaje(IDUsuario, IDViaje)
			if(datos):
				"""Le avisa al pasajero."""
				res = enviarNotificacionPush(datos, "Tu viaje fue rechazado", "Podes intentarlo con otros conductores cerca tuyo!.")
				mongo.db.log.insert({"Type": "Error", "Mensaje": str(res)})

  				response = ResponseBuilder.build_response("", '200')
			else:
				response = ErrorHandler.create_error_response(400, "No existe el viaje.")

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

	def _quitar_viaje(self, IDUsuario, IDViaje):
		"""!@brief Borra el viaje de la lista."""

		conductores = mongo.db.conductores
		res = conductores.find_and_modify({"id": IDUsuario},{"$pull": {"viajes": {"id": IDViaje}}})
		return res["datosPasajero"]["idPasajero"]
