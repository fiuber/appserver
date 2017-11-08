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
from src import mongo

class AutosPorPosicionCercana(Resource):
	"""!@brief Clase para la busqueda de autos de usuarios."""

	def __init__(self):
		self.URL = "http://fiuber-shared.herokuapp.com"
		self.autenticador = Token() 
		self.conectividad = Conectividad(self.URL)	
		self.distanciaMaxima = 50000

	def get(self):
		"""!@brief Obtiene los conductores cercanos a un determinado usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el parametro IDUsuario, POSX y POSY."""
			IDUsuario = self._validate_get_request()
			if(IDUsuario == False):
				return ErrorHandler.create_error_response(404, "Falta algun parametro.")

			"""Valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Busca en mongo los autos cercanos"""
			datos = self._obtener_autos_cercanos(self._get_param_from_request("POSX"), self._get_param_from_request("POSY"))
			if(not datos):
				return ErrorHandler.create_error_response(404, "Imposible comunicarse con mongoDB")

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
		datos = self._get_param_from_request("POSX") and self._get_param_from_request("POSY")

		if(not datos):
			return False
		else:
			return datos

	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = self.autenticador.validarToken(token)
		if(not res):
			return False
		return True

	def _obtener_autos_cercanos(self, x, y):
		"""!@brief Obtiene los autos cercanos que tenga registrados en mongoDB."""

		conductores = mongo.db.conductores
		query = "if(this.posicion){if((Math.pow(this.posicion.lng-"+str(x)+",2)+Math.pow(this.posicion.lat-"+str(y)+",2)) <= "+str(self.distanciaMaxima)+") return this}"
		return conductores.find({"$where": query})
			

	def _acondicionarAutoJSON(self, datos):
		"""!@brief Acondiciona un solo auto pasado.

		@param datos Es el auto a acondicionar."""

		return {"id": datos["id"],
			"posicion": {
				     "lng": datos["posicion"]["lng"],
				     "lat": datos["posicion"]["lat"]
				     }}

	def _acondicionarJSON(self, datos):
		"""!@brief Itera en los autos y arma el JSON.

		@param datos La response que se obtuvo del Shared Server."""


		json = {}
		i=0

		for conductor in datos:
			json[str(i)] = self._acondicionarAutoJSON(conductor)
			i += 1

		return json

		
