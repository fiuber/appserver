# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import json
import requests

from flask_restful import Resource
from flask import Flask, request

from src import URLSharedServer

class Conectividad(Resource):
	"""!@brief Clase para el manejo de las peticiones HTTP. Singleton. 
	"""
	__instance = None

	def __new__(cls, URL):
		if cls.__instance is None:
			cls.__instance= super(Conectividad,cls).__new__(cls, URL)
			cls.__instance.__initialized = False
		return cls.__instance


	def __init__(self, URL):
		"""!@brief Constructor

		@param URL URL base de todas las peticiones
		@param appServerToken El token de autenticacion del appServer"""
		if (self.__initialized): return

		app = Flask(__name__)
		self.URL = URL

		firstEndPoint = 'token'
		headers = {"Content-Type": "application/json"}
		body = {"username": "admin","password": "admin"}
		r = requests.post(URLSharedServer+'/'+firstEndPoint, data = json.dumps(body), headers = headers)
		res=json.loads(r.text)
		adminToken = res["token"]["token"]


		secondEndPoint = 'servers'
		headers = {"Authorization": "api-key "+adminToken, "Content-Type": "application/json"}
		body = {
		  "id": "string",
		  "_ref": "string",
		  "createdBy": "Agustincito",
		  "createdTime": 201710101041,
		  "name": "BestServerEver",
		  "lastConnection": 0
		}
		r = requests.post(URLSharedServer+'/'+secondEndPoint, data = json.dumps(body), headers = headers)
		res=json.loads(r.text)
		self.appServerToken = res["server"]["token"]["token"]

		self.__initialized = True

		

	def post(self, endpoint, diccionarioCuerpo = {}, diccionarioParametros = {}):
		"""!@brief Permite realizar una peticion POST y obtener el json de respuesta o false si fallo.

		@param endpoint El nombre del endpoint especifico sin la URL base ni el caracter '/'. Ej: 'user'.
		@param diccionarioCuerpo Los pares clave-valor (en forma de diccionario) a enviar en el cuerpo de la peticion.
		@param diccionarioParametros Los pares clave-valor (en forma de diccionario) a enviar como parametros de la peticion."""

		headers = {'content-type': 'application/json', 'Authorization': 'api-key '+self.appServerToken}
		r = requests.post(self.URL+'/'+endpoint,data = json.dumps(diccionarioCuerpo), headers=headers, params = diccionarioParametros)
		if(r.status_code < 200 or r.status_code > 210):
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False

	def setURL(self, URL):
		self.URL = URL
		return True

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
		if(r.status_code < 200 or r.status_code > 210):
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
		if(r.status_code < 200 or r.status_code > 210):
			return False
		else:
			try:
				return json.loads(r.text)
			except Exception as e:
				return False
			

	
