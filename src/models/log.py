# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import time
import json

from src import app
from src import mongo


class Log:
	"""!@Brief Clase para el manejo de log a mongoDB."""

	@staticmethod
	def errorLog(mensaje):
		"""!@Brief Guarda en el log como error."""

		mongo.db.log.insert({"Tipo": "Error", "Mensaje": mensaje})

		return True

	@staticmethod
	def warningLog(mensaje):
		"""!@Brief Guarda en el log como warning."""

		mongo.db.log.insert({"Tipo": "Warning", "Mensaje": mensaje})

		return True	

	@staticmethod
	def infoLog(mensaje):
		"""!@Brief Guarda en el log como info."""

		mongo.db.log.insert({"Tipo": "Info", "Mensaje": mensaje})

		return True

	@staticmethod
	def criticalLog(mensaje):
		"""!@Brief Guarda en el log como critical."""

		mongo.db.log.insert({"Tipo": "Critical", "Mensaje": mensaje})

		return True
