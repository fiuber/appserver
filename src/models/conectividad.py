# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json
import requests

from flask_restful import Resource
from flask import Flask, request

class Conectividad(Resource):
	"""!@brief Clase para el manejo de las peticiones HTTP. 
	"""

	def __init__(self, URL):
		"""!@brief Constructor

		@param URL URL base de todas las peticiones
		@param appServerToken El token de autenticacion del appServer"""

		app = Flask(__name__)
		self.URL = URL
		headers = {"Content-Type": "application/json"}
		body = {"username": "admin","password": "admin"}
		firstEndPoint = 'token'
		r = requests.post(self.URL+'/'+firstEndPoint, data = json.dumps(body), headers = headers)
		res=json.loads(r.text)
		adminToken = res["token"]["token"]

		

	def post(self, endpoint, diccionarioCuerpo = {}, diccionarioParametros = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioCuerpo Los pares clave-valor (en forma de diccionario) a enviar en el cuerpo de la peticion.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}
		r = requests.post(self.URL+'/'+endpoint,data = json.dumps(diccionarioCuerpo), headers=headers, params = diccionarioParametros)
		if(r.status_code != 200):
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False

	def get(self, endpoint, diccionarioParametros = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}
		r = requests.get(self.URL+'/'+endpoint, headers=headers, params = diccionarioParametros)
		if(r.status_code != 200):
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False

	def put(self, endpoint, diccionarioCuerpo = {}, diccionarioParametros = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioCuerpo Los pares clave-valor (en forma de diccionario) a enviar en el cuerpo de la peticion.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}
		r = requests.put(self.URL+'/'+endpoint,data = json.dumps(diccionarioCuerpo), headers=headers, params = diccionarioParametros)
		if(r.status_code != 200):
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False

	def delete(self, endpoint, diccionarioCuerpo = {}, diccionarioParametros = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioCuerpo Los pares clave-valor (en forma de diccionario) a enviar en el cuerpo de la peticion.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}
		r = requests.delete(self.URL+'/'+endpoint,data = json.dumps(diccionarioCuerpo), headers=headers, params = diccionarioParametros)
		if(r.status_code != 200):
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False
			

	
