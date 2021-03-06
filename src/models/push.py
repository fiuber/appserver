# -*- coding: utf-8 -*-
import jwt
import os
import datetime
import time
import json

from src.resources import conectividad
from src import app
from src import mongo
from src import directionsAPIKey
from src import URLGoogleDirections
from src import URLSharedServer
from src import origen


def enviarNotificacionPush(IDUsuario, titulo = "", mensaje = "", accion = 0):
	"""!@Brief Envia la notificacion push al usuario indicado."""


	URLPUSH = "https://fcm.googleapis.com/fcm"
	headers = {"content-type": "application/json",
		   "Authorization": "key=AAAAIqy7cgs:APA91bFJ1BC7rlvrQKoQNcpubZqxg_jVy1rgSH0pWxGC6Z_yN_RUAmyduc5S9j2xcC7UeLT5fy2L9bm2HGtvzYhn7daWFJgalLBxtz7ID73KprwZhQXBmZcEd05d7k_cXftN_YVifStn"}
	
	parametros = {}
	cuerpo = {"to":	"/topics/"+str(IDUsuario),
		  "data": {        "title": titulo,
				   "message": mensaje,
				   "action": accion					
				  }		
		 }

	return conectividad.post(URLPUSH, "send", cuerpo, parametros, headers)
	
