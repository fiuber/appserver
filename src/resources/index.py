# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request

from error_handler import ErrorHandler

class HelloWorld(Resource):
	
	def get(self):
		response = None
		try:
			response = '<h1><center> Bienvenido! App Server está en ejecución!</center></h1>'
			
		except Exception as e: 
			status_code = 0
			msg = "No arranca!"
			response = ErrorHandler.create_error_response(status_code, msg)

		return response