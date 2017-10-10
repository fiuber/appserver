from src.resources.auth import Auth
from models.token import Token
from mock import patch, MagicMock
import unittest
from flask import json
from server import app
import os
from flask import Flask, request, jsonify, make_response
from mocks.authorization_response import authorization_response
from resources.error_handler import ErrorHandler
from resources.response_builder import ResponseBuilder


class AuthTestCase(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_authorization(self):
		service = Auth()
		service._get_user_from_request = MagicMock(return_value='choferFranco')
		service._get_hashPassword_from_request = MagicMock(return_value='123')
		service._validate_request = MagicMock(return_value=True)
		service._existe_usuario_en_sharedServer = MagicMock(return_value=True)
		service._get_tipo = MagicMock(return_value='chofer')
		Auth.autenticador.obtenerToken = MagicMock(return_value='sefkjhskdjfhksjdf')
		ResponseBuilder.build_response = MagicMock(return_value=authorization_response)
		ErrorHandler.create_error_response = MagicMock(return_value=authorization_response)
		make_response = MagicMock(return_value=authorization_response)
		jsonify = MagicMock(return_value=authorization_response)
		#print service.post()

		self.assertEqual(service.post(), authorization_response)

