# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo

class ObtenerMetodoPago(Resource):
	"""!@brief Clase para obtener todos los metodos de pago del usuario."""


	def __init__(self):
		self.autenticador = Token() 

	def get(self, IDUsuario):
		"""!@brief Obtener los metodos de pago del usuario."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Obtener los metodos de pago."""		
			datos = self._obtener_metodopago_usuario(IDUsuario)
			if(not (type(datos) is dict)):
				return ErrorHandler.create_error_response(404, "Error al obtener metodos de pago.")
			else:
				return ResponseBuilder.build_response(datos, '200')
		
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

	def _obtener_metodopago_usuario(self, IDUsuario):
		"""!@brief Obtiene los metodos de pago de mongoDB."""
		

		resultado = mongo.db.usuarios.find_one({"id" : IDUsuario})
		if(not resultado):
			return False

		return self._acondicionarJSON(resultado.get("metodopago", {"metodopago": {"seleccionado": None}}))
		

	def _acondicionarJSON(self, metodosPago):
		"""!@brief Normaliza los datos en JSON."""

		JSONEfectivo = {}
		JSONTarjeta = {}

		"""Puede quedar vacio el JSON final si no tiene metodos de pago configurados."""

	
		JSONEfectivo = {"moneda": metodosPago.get("efectivo",{}).get("moneda",{})}


		try:
			JSONTarjeta = {"moneda": metodosPago["tarjeta"]["moneda"],
				       "numero": metodosPago["tarjeta"]["numero"],
				       "fechaVencimiento": metodosPago["tarjeta"]["fechaVencimiento"],
				       "cvv": metodosPago["tarjeta"]["cvv"]}
		except Exception as e:
			JSONTarjeta = {}

		JSON = {"seleccionado": metodosPago.get("seleccionado")}
		
		if(JSONEfectivo["moneda"]):
			JSON["efectivo"] = JSONEfectivo
	
		if(JSONTarjeta):
			JSON["tarjeta"] = JSONTarjeta
		

		return JSON



