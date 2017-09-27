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
		tipo = self._get_type_from_request()
		usr = self._get_usr_from_request()
		pwd = self._get_pwd_from_request()
		fb = self._get_fb_from_request()
		name = self._get_name_from_request()
		lastname = self._get_lastname_from_request()
		email = self._get_email_from_request()
		birthdate = self._get_birthdate_from_request()

		user = User(tipo, usr, pwd, fb, name, lastname, email, birthdate)

		if (user.exists()):
			ErrorHandler.create_error_response("409", "Usuario o mail ya existente.")
		else:
			id = user.stored_user_in_shared_server()
			return ResponseBuilder.build_response(id)




	def _get_type_from_request(self):
		"""!@brief Obtiene el tipo(passenger o driver) de la request. 
		"""
		return request.get_json()["type"]

	def _get_usr_from_request(self):
		"""!@brief Obtiene el nombre de usuario de la request. 
		"""
		return request.get_json()["username"]

	def _get_pwd_from_request(self):
		"""!@brief Obtiene la contraseña del usuario de la request. 
		"""
		return request.get_json()["password"]

	def _get_fb_from_request(self):
		"""!@brief Obtiene la contraseña del usuario de la request. 
		"""
		return request.get_json()["fb"]

	def _get_name_from_request(self):
		"""!@brief Obtiene el/los nombres de la request. 
		"""
		return request.get_json()["firstName"]

	def _get_lastname_from_request(self):
		"""!@brief Obtiene el/los apellidos de la request. 
		"""
		return request.get_json()["lastName"]

	def _get_email_from_request(self):
		"""!@brief Obtiene el email de la request. 
		"""
		return request.get_json()["email"]

	def _get_birthdate_from_request(self):
		"""!@brief Obtiene la fecha de nacimiento de la request. 
		"""
		return request.get_json()["birthdate"]


		