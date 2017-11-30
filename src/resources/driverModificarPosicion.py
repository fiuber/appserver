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
from src.models.push import enviarNotificacionPush
from src.resources import conectividad
from src.models.log import Log
from geopy.distance import vincenty

from error_handler import ErrorHandler
from response_builder import ResponseBuilder
from src import app
from src import mongo
from src import origen
from src import URLSharedServer
from src import PUSHViajeTerminadoChofer
from src import PUSHViajeTerminadoPasajero

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

		pasajero = None
		viaje = None
		try:
			viaje = mongo.db.viajes.find_one({"IDConductor": datosConductor["id"]})
			if(not viaje):
				return False

			pasajero = mongo.db.usuarios.find_one({"id": viaje["IDPasajero"]})
			if(not pasajero):
				return False
				
		except Exception as e:
			return False

		"""Si estan muy cerca y no estaban en viaje todavia se asume que ya empezo."""

		terminoEspera = False
		terminoViaje = False
		posicionConductor = {}
		try:
			posicionConductor = {"lng": x,"lat": y}

			if(datosConductor["estado"] == "recogiendoPasajero"):
				posicionPasajero = pasajero["posicion"]
				distancia = (posicionConductor["lng"]-posicionPasajero["lng"])**2+(posicionConductor["lat"]-posicionPasajero["lat"])**2
				if(distancia < self.distanciaMinima):
					if(pasajero["estado"] == "esperandoChofer") :
						res = mongo.db.usuarios.update({"id": pasajero["id"]},{"$set": {"estado": "libre"}})
						if(res["nModified"] == 0):
							return False

					if(datosConductor["estado"] == "recogiendoPasajero"):
						res = mongo.db.conductores.update({"id": datosConductor["id"]},{"$set": {"estado": "libre"}})
						if(res["nModified"] == 0):
							return False
						
					terminoEspera = True

		except Exception as e:
			terminoEspera = False

		distanciaDestino = (posicionConductor["lng"]-viaje["destino"]["lng"])**2+(posicionConductor["lat"]-viaje["destino"]["lat"])**2

		if(distanciaDestino < self.distanciaMinima and viaje["timestampFinViaje"] == 0):
			terminoViaje = True
		
		tiempoPosicion = time.time()
		nuevaPosicionGrados = {"timestamp": tiempoPosicion,
				    "location": {"lon": xlon,
				     		 "lat": ylat}
					}

		nuevaPosicionMetros = {"timestamp": tiempoPosicion,	 
					  "location": {"lng": x,
					   	       "lat": y}
					} 				   
				 

		updateQuery = {"$push": 
				{"rutaConductor": nuevaPosicionMetros,					
				 "rutaConductorGrados": nuevaPosicionGrados
				}
			      }		

		if(terminoEspera):
			updateQuery["$set"] = {"timestampFinEspera": time.time()}
		elif(terminoViaje):	
			if(pasajero["estado"] != "libre"):
				res = mongo.db.usuarios.update({"id": pasajero["id"]},{"$set": {"estado": "libre"}})
				if(res["nModified"] == 0):
					return False

			if(datosConductor["estado"] != "libre"):
				res = mongo.db.conductores.update({"id": datosConductor["id"]},{"$set": {"estado": "libre"}})
				if(res["nModified"] == 0):
					return False

			tiempoFinViaje = time.time()

			"""Finalizar viaje con Shared Server."""

			viaje["rutaConductor"].append(nuevaPosicionMetros)
			viaje["rutaConductorGrados"].append(nuevaPosicionGrados)
		
			if(not self._finalizar_viaje_shared(viaje, tiempoFinViaje)):
				return False

			updateQuery["$set"] = {"timestampFinViaje": tiempoFinViaje}


		if(viaje["timestampFinViaje"] == 0):
			res = mongo.db.viajes.update({"IDConductor": datosConductor["id"]}, updateQuery)
			if(res["nModified"] == 0):
				return False

		return True

	def calcularDistanciaFinal(self, puntos):
		listaOrdenada = sorted(puntos, key=lambda punto: punto["timestamp"])
		distanciaFinal = 0

		
		for i in range(0, len(listaOrdenada)-2):
			distancia = (listaOrdenada[i]["location"]["lng"]-listaOrdenada[i+1]["location"]["lng"])**2 + (listaOrdenada[i]["location"]["lat"]-listaOrdenada[i+1]["location"]["lat"])**2
			distanciaFinal = distanciaFinal + distancia
		return distanciaFinal

	def _finalizar_viaje_shared(self, viaje, tiempoFinViaje):
		"""!@brief Agrega el viaje terminado al Shared Server."""

		viaje["origenGrados"]["lon"] = viaje["origenGrados"].pop("lng")
		viaje["destinoGrados"]["lon"] = viaje["destinoGrados"].pop("lng")

		trip = {"id": "",
			"cost": {"currency": "ARS", "value": 0},
			"applicationOwner": "",
			"driver": viaje["IDConductor"],
			"passenger": viaje["IDPasajero"],
			"start": {"address": {"location": viaje["origenGrados"]},
				  "timestamp": viaje["timestampInicio"]},
			"end": {"address": {"location": viaje["destinoGrados"]},
				  "timestamp": tiempoFinViaje},
			"totalTime": (tiempoFinViaje - viaje["timestampInicio"]),
			"waitTime": (viaje["timestampFinEspera"] - viaje["timestampInicio"]),
			"travelTime": (tiempoFinViaje - viaje["timestampFinEspera"]),
			"route": viaje["rutaConductorGrados"],
			"distance": self.calcularDistanciaFinal(viaje["rutaConductor"])}


		"""Configura el medio de pago."""
		usuario = mongo.db.usuarios.find_one({"id": viaje["IDPasajero"]})

		if(not usuario):
			return False

		"""Si no tiene seleccionado un metodo de pago setea efectivo en pesos como default."""
		metodo = usuario.get("metodopago",{}).get("seleccionado","efectivo")
		if(metodo == "tarjeta"):
			metodo = "card"
		else:
			metodo = "cash"

		fecha = usuario.get("metodopago",{}).get("tarjeta",{}).get("fechaVencimientos","1-2")
		fecha = fecha.split("-")

		pago = {}
		if(metodo == "card"):
			pago = {"paymethod": metodo,
				"parameters": {"ccvv": usuario["metodopago"]["tarjeta"]["cvv"],
					       "expiration_month": fecha[0],
					       "expiration_year": fecha[1],
					       "number": usuario["metodopago"]["tarjeta"]["numero"],
					       "type": usuario["metodopago"]["tarjeta"]["moneda"]
					      }
			       } 
		elif(metodo == "cash"):
			pago = {"paymethod": metodo,
				"parameters": {"type": usuario.get("metodopago",{}).get("efectivo",{}).get("moneda","ARS")}} 

		res = conectividad.post(URLSharedServer, "trips", {"trip": trip, "paymethod": pago})
		if(not res):
			return False
		


		"""Envia las notificaciones push"""
		self._informar_viaje(viaje["IDPasajero"], viaje["IDConductor"])		

		return True
		

	def _actualizar_posicion_conductor(self, IDUsuario, xlon, ylat):

		"""Convierte a metros"""

		x = vincenty((0,xlon), origen).meters
		y = vincenty((ylat,0), origen).meters

		datosConductor = mongo.db.conductores.find_and_modify({"id" : IDUsuario}, {"$set": {"posicion" : {"lng": x, "lat": y}}}, upsert=True, new=True)
		if(not datosConductor):
			return False

		"""Si esta en un viaje actualiza los datos del mismo."""
		self._actualizar_datos_viaje(datosConductor, x, y, xlon, ylat)

		return True

	def _informar_viaje(self, IDPasajero, IDConductor):
		"""!@Brief Envia la notificacion push al conductor y al pasajero para avisarle que puede aceptar un viaje."""

		enviarNotificacionPush(IDPasajero, "Termino el viaje!", "Llegaste a destino.", PUSHViajeTerminadoPasajero)
		enviarNotificacionPush(IDConductor, "Termino el viaje!", "Llegaste a destino.", PUSHViajeTerminadoChofer)

		return True
	


