# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import time
import json

from src.models.conectividad import Conectividad
from src import app
from src import mongo


def errorLog(mensaje):
	"""!@Brief Guarda en el log como error."""

	mongo.db.log.insert({"Tipo": "Error", "Mensaje": mensaje})

	return True

def warningLog(mensaje):
	"""!@Brief Guarda en el log como warning."""

	mongo.db.log.insert({"Tipo": "Warning", "Mensaje": mensaje})

	return True	

def infoLog(mensaje):
	"""!@Brief Guarda en el log como info."""

	mongo.db.log.insert({"Tipo": "Info", "Mensaje": mensaje})

	return True

def criticalLog(mensaje):
	"""!@Brief Guarda en el log como critical."""

	mongo.db.log.insert({"Tipo": "Critical", "Mensaje": mensaje})

	return True
