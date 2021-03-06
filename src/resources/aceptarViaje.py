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
from src.models.log import Log

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo
from src import URLSharedServer
from src import PUSHViajeAceptado
from src import PUSHRechazoViaje

class AceptarViaje(Resource):
	"""!@brief Clase para aceptar un viaje de un chofer."""


	def __init__(self):
		self.autenticador = Token() 

	def post(self, IDUsuario, IDViaje):
		"""!@brief Acepta un viaje y borra todos los otros."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")
			"""Devuelve los posibles viajes."""
			datos = self._aceptar_viaje(IDUsuario, IDViaje)
			if(datos):
				"""Le avisa al pasajero."""
				res = enviarNotificacionPush(datos, "Viaje aceptado!", "El conductor se dirige a tu ubicacion.", PUSHViajeAceptado)

  				response = ResponseBuilder.build_response({}, '200')
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

	def dar_alta(self, viaje, IDUsuario):
		"""!@brief Da de alta el viaje en el Shared Server."""

		JSON = {"IDConductor": IDUsuario,
			"IDPasajero": viaje["datosPasajero"]["idPasajero"],
			"origen": viaje["origen"],
			"origenGrados": viaje["origenGrados"],
			"destino": viaje["destino"],
			"destinoGrados": viaje["destinoGrados"],
			"timestampFinEspera": 0,
			"timestampFinViaje": 0,
			"timestampInicio": time.time(),
			"rutaConductor":[]}

		try:
			viajes = mongo.db.viajes
			viajes.insert(JSON)

		except Exception as e:
			return False
		return True

		

	def _aceptar_viaje(self, IDUsuario, IDViaje):
		"""!@brief Acepta un viaje."""

		conductores = mongo.db.conductores
		usuarios = mongo.db.usuarios

		"""Obtiene los datos del viaje."""
		viaje = conductores.find_one({"id": IDUsuario},{"viajes": {"$elemMatch": {"idViaje": IDViaje}}})

		if(not viaje):
			return False

		viaje = viaje["viajes"][0]
		
		"""Reserva el viaje (Solo el primero en llegar se procesa asi se evitan colisiones)."""
		res = usuarios.update({"id": viaje["datosPasajero"]["idPasajero"], "estado": "libre"}, {"$set": {"estado": "esperandoChofer"}})
		if(res["nModified"] == 0):
			return False
		
		"""Libera a todos los otros choferes (les borra viajes de este usuario)."""
		conductores.update({"id": {"$ne": IDUsuario}}, {"$pull": {"viajes": {"datosPasajero.idPasajero": viaje["datosPasajero"]["idPasajero"]}}})

		"""Configura el estado del conductor asignado a recogiendoPasajero"""
		conductores.update({"id": IDUsuario},{"$set": {"estado": "recogiendoPasajero"}})

		"""Da el alta al viaje en mongoDB."""
		res = self.dar_alta(viaje, IDUsuario)
		if(not res):
			return False

		"""Finalmente borra todos los viajes disponibles del chofer (No puede tomar mas)."""
		res = True
		
		"""Avisa del rechazo de los viajes"""
		cond = conductores.find_one({"id": IDUsuario})
		for x in cond.get("viajes",[]):
			if(x["datosPasajero"]["idPasajero"] != viaje["datosPasajero"]["idPasajero"]):
				enviarNotificacionPush(x["datosPasajero"]["idPasajero"], "Tu viaje fue rechazado", "Podes intentarlo con otros conductores cerca tuyo!.", PUSHRechazoViaje)

		conductores.update({"id": IDUsuario},{"$set": {"viajes": []}})		

		return viaje["datosPasajero"]["idPasajero"]
		


