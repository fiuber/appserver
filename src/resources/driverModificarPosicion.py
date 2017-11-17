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
from src import origen

class ConductorModificarPosicion(Resource):
	"""!@brief Clase para actualizar la posicion de un conductor."""


	def __init__(self):
		self.autenticador = Token() 
		self.distanciaMinima = 36**2


	def put(self, IDUsuario):
		"""!@brief Actualiza los datos de posicion de un conductor."""
		response = ResponseBuilder.build_response({}, '200')
		try:
			"""Valida que este el JSON con los datos de la posicion."""
			valid = self._validate_request()
			if(not valid):
				return ErrorHandler.create_error_response(500, "Faltan parametros.")

			"""Primero valida el token."""
			if(not self._validar_token()):
				return ErrorHandler.create_error_response(400, "Token expirado o incorrecto.")

			"""Actualiza la posicion."""
			pos = self._get_data_from_request("posicion")

			if(not self._actualizar_posicion_conductor(IDUsuario, pos["lng"], pos["lat"])):
				return ErrorHandler.create_error_response(500, "No se pudo actualizar la posicion.")


		except Exception as e:
			status_code = 403
			msg = str(e)
			response = ErrorHandler.create_error_response(status_code, msg)
		return response

	def _get_data_from_request(self, nombrePropiedad):
		"""!@brief Obtiene la propiedad del json contenido de la request."""

		try:
			return request.get_json()[nombrePropiedad]
		except Exception as e:
			return False

	def _validate_request(self):
		"""!@brief Valida que haya una request completa."""

		res = self._get_data_from_request("posicion")

		if(not res):
			return False
		else:
			return True

	def _validar_token(self):
		"""!@brief Valida al usuario."""

		token = request.headers.get("Authorization").split(" ")[1]

		res = self.autenticador.validarToken(token)
		if(not res):
			return False
		return True

	def _actualizar_datos_viaje(self, datosConductor, x, y, xlon, ylat):
		"""!@brief Modifica los parametros del viaje en curso si corresponde."""

		if(datosConductor["estado"] == "libre"):
			return True

		viajes = mongo.db.viajes
		conductores = mongo.db.conductores
		pasajeros = mongo.db.usuarios


		pasajero = None
		viaje = None
		try:
			viaje = viajes.find_one({"IDConductor": datosConductor["id"]})
			if(not viaje):
				return False

			pasajero = pasajeros.find_one({"id": viaje["IDPasajero"]})
			if(not pasajero):
				return False
				
		except Exception as e:
			return False

		"""Si estan muy cerca y no estaban en viaje todavia se asume que ya empezo."""

		terminoEspera = False
		terminoViaje = False
		posicionConductor = {}
		try:
			posicionConductor = datosConductor["posicion"]

			if(datosConductor["estado"] == "recogiendoPasajero"):
				posicionPasajero = pasajero["posicion"]
				distancia = (posicionConductor["lng"]-posicionPasajero["lng"])**2+(posicionConductor["lat"]-posicionPasajero["lat"])**2
				if(distancia < self.distanciaMinima):
					res = pasajeros.update({"id": pasajero["id"]},{"$set": {"estado": "viajando"}})
					if(res["nModified"] != 0):
						conductores.update({"id": datosConductor["id"]},{"$set": {"estado": "viajando"}})
			elif(viaje["timestampFinEspera"] == 0):
				terminoEspera = True					


		except Exception as e:
			terminoEspera = False

		distanciaDestino = (posicionConductor["lng"]-viaje["destino"]["lng"])**2+(posicionConductor["lat"]-viaje["destino"]["lat"])**2

		if(distanciaDestino < self.distanciaMinima and viaje["timestampFinViaje"] == 0):
			terminoViaje = True
		
		tiempoPosicion = time.time()
		nuevaPosicionMetros = {"timestamp": tiempoPosicion,
				    "location": {"lon": xlon,
				     		 "lat": ylat}
					}

		nuevaPosicionGrados = {"timestamp": tiempoPosicion,	 
					  "location": {"lng": x,
					   	       "lat": y}
					} 				   
				 

		updateQuery = {"$push": 
				{"rutaConductor": nuevaPosicionGrados,					
				 "rutaConductorGrados": nuevaPosicionMetros
				}
			      }		

		if(terminoEspera):
			updateQuery["$set"] = {"timestampFinEspera": time.time()}
		elif(terminoViaje):	
	
			res = pasajeros.update({"id": pasajero["id"]},{"$set": {"estado": "libre"}})
			if(res["nModified"] != 0):
				conductores.update({"id": datosConductor["id"]},{"$set": {"estado": "libre"}})

			tiempoFinViaje = time.time()

			"""Finalizar viaje con Shared Server."""	

			viaje["rutaConductor"].append(nuevaPosicionMetros)
			viaje["rutaConductorGrados"].append(nuevaPosicionGrados)
		
			if(not self._finalizar_viaje_shared(viaje, tiempoFinViaje)):
				return False

			updateQuery["$set"] = {"timestampFinViaje": tiempoFinViaje}


		if(viaje["timestampFinViaje"] == 0):
			res = viajes.update({"IDConductor": datosConductor["id"]}, updateQuery)
			if(res["nModified"] == 0):
				return False
		return True

	def calcularDistanciaFinal(self, puntos):
		listaOrdenada = sorted(puntos, key=lambda punto: punto["timestamp"])
		distanciaFinal = 0

		for i in range(0, len(listaOrdenada)):
			distancia = (listaOrdenada[i]["location"]["lng"]-listaOrdenada[i+1]["location"]["lng"])**2 + (listaOrdenada[i]["location"]["lat"]-listaOrdenada[i+1]["location"]["lat"])**2
			distanciaFinal = distanciaFinal + distancia

		return distanciaFinal

	def _finalizar_viaje_shared(self, viaje, tiempoFinViaje):
		"""!@brief Agrega el viaje terminado al Shared Server."""

		trip = {"driver": viaje["IDConductor"],
			"passenger": viaje["IDPasajero"],
			"start": {"address": {"location": viaje["origenGrados"]},
				  "timestamp": viaje["timestampInicio"]},
			"end": {"address": {"location": viaje["destinoGrados"]},
				  "timestamp": tiempoFinViaje},
			"totaTime": (tiempoFinViaje - viaje["timestampInicio"]),
			"waitTime": (viaje["timestampFinEspera"] - viaje["timestampInicio"]),
			"travelTime": (tiempoFinViaje - viaje["timestampFinEspera"]),
			"route": viaje["rutaConductorGrados"],
			"distance": self.calcularDistanciaFinal(viaje["rutaConductor"])}
		

		return True
		

	def _actualizar_posicion_conductor(self, IDUsuario, xlon, ylat):
		conductores = mongo.db.conductores

		"""Convierte a metros"""

		x = vincenty((0,xlon), origen).meters
		y = vincenty((ylat,0), origen).meters

		datosConductor = conductores.find_and_modify({"id" : IDUsuario}, {"$set": {"posicion" : {"lng": x, "lat": y}}}, upsert=True, new=True)
		if(not datosConductor):
			return False

		"""Si esta en un viaje actualiza los datos del mismo."""
		self._actualizar_datos_viaje(datosConductor, x, y, xlon, ylat)

		return True


