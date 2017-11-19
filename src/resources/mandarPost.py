# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import time
import json

from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo
from src.models.token import Token
from src.models.conectividad import Conectividad
from geopy.distance import vincenty

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo
from src import directionsAPIKey
from src import URLGoogleDirections
from src import URLSharedServer
from src import origen

class MandarPost(Resource):
	"""!@brief Clase para mandar al usuario una notificacion."""


	def __init__(self):
		self.autenticador = Token() 
		self.conectividad = Conectividad(URLSharedServer)

	def post(self, IDUsuario):
		"""!@brief Le manda al usuario una notificacion."""

		try:
			self._informar_viaje(IDUsuario)
		except Exception as e:
			return ResponseBuilder.build_response(str(e), '200')

		return ResponseBuilder.build_response("Salio OK", '200')


	def _informar_viaje(self, IDUsuario):
		"""!@Brief Envia la notificacion push al conductor para avisarle que puede aceptar un viaje."""

		URLPUSH = "https://fcm.googleapis.com/fcm"
		self.conectividad.setURL(URLPUSH)
		headers = {"content-type": "application/json",
			   "Authorization": "key=AAAAIqy7cgs:APA91bFJ1BC7rlvrQKoQNcpubZqxg_jVy1rgSH0pWxGC6Z_yN_RUAmyduc5S9j2xcC7UeLT5fy2L9bm2HGtvzYhn7daWFJgalLBxtz7ID73KprwZhQXBmZcEd05d7k_cXftN_YVifStn"}
		
		parametros = {}
		cuerpo = {"to":	"/topics/"+IDUsuario,
			  "notification": {"title": "Nuevo viaje disponible",
					   "text": "Tenes un nuevo viaje para aceptar!"
					  }		
			 }
		
		self.conectividad.post("send", cuerpo, parametros, headers)

		return True
	
