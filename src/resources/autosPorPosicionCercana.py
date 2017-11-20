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
from geopy.distance import vincenty

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo
from src import origen
from src import URLSharedServer

class AutosPorPosicionCercana(Resource):
	"""!@brief Clase para la busqueda de autos de usuarios."""

	def __init__(self):
		self.autenticador = Token() 
		self.distanciaMaxima = 5000**2
		self.conectividad = Conectividad(URLSharedServer)

	def get(self):
		"""!@brief Obtiene los conductores cercanos a un determinado usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el parametro lng y lat."""
			res = self._validate_get_request()
			if(res == False):
				return ErrorHandler.create_error_response(404, "Falta algun parametro.")

			"""Valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Busca en mongo los autos cercanos"""
			datos = self._obtener_autos_cercanos(self._get_param_from_request("lng"), self._get_param_from_request("lat"))

			"""Devuelve el JSON acondicionado.""" 
			datos = self._acondicionarJSON(datos)
			response = ResponseBuilder.build_response(datos, '200')

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response


	def _get_param_from_request(self, nombreParametro):
		"""!@brief Obtiene el parametro dado de la request."""
		return request.args.get(nombreParametro)


	def _validate_get_request(self):
		"""!@brief Tiene que estar la posicion del usuario que realiza la busqueda."""
		datos = self._get_param_from_request("lng") and self._get_param_from_request("lat")

		if(not datos):
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

	def _obtener_autos_cercanos(self, x, y):
		"""!@brief Obtiene los autos cercanos que tenga registrados en mongoDB."""

		"""Convierte a metros"""

		x = vincenty((0,x), origen).meters
		y = vincenty((y,0), origen).meters
		
		conductores = mongo.db.conductores
		query = "if(this.posicion){if((Math.pow(this.posicion.lng-"+str(x)+",2)+Math.pow(this.posicion.lat-"+str(y)+",2)) <= "+str(self.distanciaMaxima)+") return this}"
		return conductores.find({"$where": query})	
			

	def _acondicionarAutoJSON(self, datos):
		"""!@brief Acondiciona un solo auto pasado.

		@param datos Es el auto a acondicionar."""

		"""Le pide los datos al Shared Server."""

		autoActivo = mongo.db.conductores.find_one({"id": datos["id"]})

		"""Si el usuario no tiene auto activo no se muestra."""
		if(not autoActivo.get("autoActivo",False)):
			return False

		self.conectividad.setURL(URLSharedServer)
		
		URLDestino = "users/"+datos["id"]+"/cars/"+autoActivo["autoActivo"]

		datos = self.conectividad.get(URLDestino)
		if(not datos):
			raise Exception("No existe el usuario")

		dato = datos["car"]["properties"]
				
		JSON = {}

		for prop in dato:
			JSON[prop["name"]] = prop["value"] 


		return {"id": datos["car"]["id"],
			"perfil": JSON
	               }

	def _acondicionarJSON(self, datos):
		"""!@brief Itera en los autos y arma el JSON.

		@param datos La response que se obtuvo de mongoDB."""

		json = {}
		i=0

		for conductor in datos:
			auto = self._acondicionarAutoJSON(conductor)
			if(auto):
				json[str(i)] = auto
				i += 1

		return json

		
