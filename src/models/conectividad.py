# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json
import requests
import time

from flask_restful import Resource
from flask import Flask, request

from src.models.log import Log

from src import URLSharedServer
from src import mongo
from src import app

class Conectividad(Resource):
	"""!@brief Clase para el manejo de las peticiones HTTP. Singleton. 
	"""

	def __init__(self):

		with app.app_context():
			token = mongo.db.token.find_one({"id": 1})

			self.ultimaVez = time.time()
			self.appServerToken = token["token"]

	def post(self, URL, endpoint, diccionarioCuerpo = {}, diccionarioParametros = {}, diccionarioHeader = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioCuerpo Los pares clave-valor (en forma de diccionario) a enviar en el cuerpo de la peticion.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		self.renovarToken()

		if(diccionarioHeader):
			headers = diccionarioHeader
		else:
			headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}

		r = requests.post(URL+'/'+endpoint,data = json.dumps(diccionarioCuerpo), headers=headers, params = diccionarioParametros)
		if(r.status_code < 200 or r.status_code > 210):
			Log.errorLog("POST: " + str(r) + " - " + endpoint + " - " + URL + " - " + str(diccionarioCuerpo))
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False

	def get(self, URL, endpoint, diccionarioParametros = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		self.renovarToken()

		headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}
		r = requests.get(URL+'/'+endpoint, headers=headers, params = diccionarioParametros)
		if(r.status_code != 200):
			Log.errorLog("GET: " + str(r) + " - " + endpoint + " - " + str(diccionarioParametros) + " - " + URL)
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False

	def put(self, URL, endpoint, diccionarioCuerpo = {}, diccionarioParametros = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioCuerpo Los pares clave-valor (en forma de diccionario) a enviar en el cuerpo de la peticion.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		self.renovarToken()

		headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}
		r = requests.put(URL+'/'+endpoint,data = json.dumps(diccionarioCuerpo), headers=headers, params = diccionarioParametros)
		if(r.status_code < 200 or r.status_code > 210):
			Log.errorLog("PUT: " + str(r) + " - " + endpoint + " - " + str(diccionarioParametros) + " - " + URL+ " - " + str(diccionarioCuerpo))
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False

	def delete(self, URL, endpoint, diccionarioCuerpo = {}, diccionarioParametros = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioCuerpo Los pares clave-valor (en forma de diccionario) a enviar en el cuerpo de la peticion.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		self.renovarToken()

		headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}
		r = requests.delete(URL+'/'+endpoint,data = json.dumps(diccionarioCuerpo), headers=headers, params = diccionarioParametros)
		if(r.status_code < 200 or r.status_code > 210):
			Log.errorLog("DELETE: " + str(r) + " - " + endpoint + " - " + str(diccionarioParametros) + " - " + URL + " - " + str(diccionarioCuerpo))
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return True

	def renovarToken(self):
		"""!@brief Renueva el token si pasaron 5 horas."""

		if((time.time() - self.ultimaVez) > 5*60*60):
			self.ultimaVez = time.time()
			data = self.post(URLSharedServer, "servers/ping")
			if(data):
				self.appServerToken = data["ping"]["token"]["token"]
				mongo.db.token.update({"id": 1},{"token": self.appServerToken},upsert=True)
			
