# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request

from error_handler import ErrorHandler
from response_builder import ResponseBuilder

class Token(Resource):

	def post(self):
		response = None
		try:
			user = self._get_user_from_request()
			hashPassword = self._get_hashPassword_from_request()
			response = ResponseBuilder.build_response(self._get_token(user, hashPassword), '200')

		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response

	def _get_user_from_request(self):
		return request.get_json()["nombreUsuario"]
	
	def _get_hashPassword_from_request(self):
		return request.get_json()["contrasenia"]
	
	# hacer funcion, deberiamos crear una clase Token, ponerla en la carpeta Models, y que acceda a la db
	def _get_token(self, user, hashPassword):
		return { "token" : "askjhfakefjhefrbqjbe3rh839" }