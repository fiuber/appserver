# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import Flask, request

from error_handler import ErrorHandler
from response_builder import ResponseBuilder

from src.models.user import User

class Register(Resource):
	"""!@brief Clase para registro de nuevo usuario. 
	"""
	
	def post(self):
		"""!@brief Post: agrega un usuario.
		"""
	
		try:
			tipo = request.get_json()["type"]
			usr = request.get_json()["username"]
			pwd = request.get_json()["password"]
			fb = request.get_json()["fb"]
			name = request.get_json()["firstName"]
			lastname = request.get_json()["lastName"]
			email = request.get_json()["email"]
			birthdate = request.get_json()["birthdate"]
			
		except Exception as e:
			return ErrorHandler.create_error_response("400", "Bad Request. Header incorrecto.")

		user = User(tipo, usr, pwd, fb, name, lastname, email, birthdate)

		if (user.exists_by_username()):
			return ErrorHandler.create_error_response("409", "Usuario o mail ya existente.")
		
		else:
			msg = user.stored_user_in_shared_server()
			return ResponseBuilder.build_response({"msg": msg})


class UserController(Resource):
	"""!@brief Clase para modificar, eliminar y obtener un usuario. 
	"""

	def put(self, userId):
		"""!@brief Put: modifica un usuario. 
		"""
		try:
			tipo = request.get_json()["type"]
			usr = request.get_json()["username"]
			pwd = request.get_json()["password"]
			fb = request.get_json()["fb"]
			name = request.get_json()["firstName"]
			lastname = request.get_json()["lastName"]
			email = request.get_json()["email"]
			birthdate = request.get_json()["birthdate"]

		except Exception as e:
			return ErrorHandler.create_error_response("400", "Bad Request. Header incorrecto.")

		user = User(tipo, usr, pwd, fb, name, lastname, email, birthdate)

		if not (user.exists_by_username()):
			return ErrorHandler.create_error_response("404", "No existe el usuario")
		else:
			msg = user.modify_user_in_shared_server()
			return ResponseBuilder.build_response({"msg":msg})

	def get(self, userId):
		"""!@brief Get: obtiene info de un usuario.
		"""
		user = User(None, userId, None, None, None, None, None, None)
		if not (user.exists_by_username()):
			return ErrorHandler.create_error_response("409", "No existe el Id")
		else:
			return ResponseBuilder.build_response(userId) # debe llamar al shared y pedirle la info


	def delete(self, userId):
		"""!@brief Delete: elimina un usuario. 
		"""

		user = User(None, userId, None, None, None, None, None, None)
		if not (user.exists_by_username()):
			return ErrorHandler.create_error_response("409", "No existe el Id")
		else:
			return ResponseBuilder.build_response(userId) # debe llamar al shared y borrarlo
