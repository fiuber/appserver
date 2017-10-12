# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import Flask, request

from error_handler import ErrorHandler
from response_builder import ResponseBuilder

from src.models.user import User
from src.models.conectividad import Conectividad


class Register(Resource):
	"""!@brief Clase para registro de nuevo usuario. 
	"""
	def get(self):
		connect = Conectividad("https://fiuber-shared.herokuapp.com")
		res = connect.get("users", {})
		return ResponseBuilder.build_response(res, 200)

	
	def post(self):
		"""!@brief Post: agrega un usuario.
		"""
		connect = Conectividad("https://fiuber-shared.herokuapp.com")
		try:
			body = {
				"_ref": "907.0558422010005", #mal
				"type": request.get_json()["type"],
				"username": request.get_json()["username"],
				"password": request.get_json()["password"],
				"firstName": request.get_json()["firstName"],
				"lastName": request.get_json()["lastName"],
				"country": request.get_json()["country"],
				"email": request.get_json()["email"],
				"birthdate": request.get_json()["birthdate"],
				"images": ["1.png","2.png","3.png"]
			}
			
			
		except Exception as e:
			return ErrorHandler.create_error_response("400", "Bad Request. Header incorrecto.")

		res = connect.post("users", body, {})

		return ResponseBuilder.build_response(res, 201)


class UserController(Resource):
	"""!@brief Clase para modificar, eliminar y obtener un usuario. 
	"""

	def put(self, userId):
		"""!@brief Put: modifica un usuario. 
		"""
		connect = Conectividad("https://fiuber-shared.herokuapp.com")
		userId = "6" # el del ref harcodeado de abajo
		try:
			body = {
				"_ref": "610.6623890863641",  # donde lo deberia tomar?????
				"type": request.get_json()["type"],
				"username": request.get_json()["username"],
				"password": request.get_json()["password"],
				"firstName": request.get_json()["firstName"],
				"lastName": request.get_json()["lastName"],
				"country": request.get_json()["country"],
				"email": request.get_json()["email"],
				"birthdate": request.get_json()["birthdate"],
				"images": ["1.png","2.png","3.png"]
			}

		except Exception as e:
			return ErrorHandler.create_error_response("400", "Bad Request. Header incorrecto.")

		res = connect.put("users/"+userId, body, {})

		return ResponseBuilder.build_response(res, 200)

	def get(self, userId):
		"""!@brief Get: obtiene info de un usuario.
		"""
		connect = Conectividad("https://fiuber-shared.herokuapp.com")

		res = connect.get("users/"+userId, {})

		responseJson = {
			"name": res["user"]["name"],
			"surname": res["user"]["surname"],
			"email": res["user"]["email"],
			"birthdate": res["user"]["birthdate"],
			"cars": res["user"]["cars"],
			"country": res["user"]["country"],
			"username": res["user"]["username"]
		}
		
		return ResponseBuilder.build_response(responseJson, 200)


	def delete(self, userId):
		"""!@brief Delete: elimina un usuario. 
		"""
		connect = Conectividad("https://fiuber-shared.herokuapp.com")

		res = connect.delete("users/"+userId, {}, {})

		return ResponseBuilder.build_response(res, 204)
