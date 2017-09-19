import json
import jwt
import os
import datetime
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'fiuberappserver'
app.config['MONGO_URI'] = 'mongodb://fiuberappserver:fiuberappserver@ds123534.mlab.com:23534/fiuberappserver'
mongo = PyMongo(app)

def generarToken(nombreUsuario, contrasena):
	"""!@brief Genera y devuelve el token de autenticacion del usuario con el appserver
	@param nombreUsuario Nombre del usuario.
	@param contrasena Contrasena del usuario hasheada.
	"""
	try:

		"""
		En el payload estan los datos propiamente dichos		
		"""
		payload = {
		    'exp': datetime.datetime.utcnow() + datetime.timedelta(days = 1),
		    'iat': datetime.datetime.utcnow(),
		    'nombreUsuario': nombreUsuario,
		    'contrasena': contrasena
		}
		return jwt.encode(
		    payload,
		    os.urandom(24),
		    algorithm = 'HS256'
		)
	except Exception as e:
		return False

def almacenarToken(nombreUsuario, token):
	"""!@brief Guarda el token en mongoDB para accederlo de una. 
	Devuelve true si se pudo guardar o false si no se pudo porque no existia el usuario
	
	@param nombreUsuario Nombre del usuario.
	@param token token a guardar.
	"""

	usuarios = mongo.db.usuarios
	usuario = usuario.find_one({'nombreUsuario': nombreUsuario})
	if(usuario):
		usuarios.insert({"nombreUsuario" : nombreUsuario, "token": token})
		return True
	else:
		return False


def recuperarToken(nombreUsuario):
	"""!@brief Recupera el token de mongoDB. 
	Devuelve el token o false.
	
	@param nombreUsuario Nombre del usuario.
	"""

	usuarios = mongo.db.usuarios
	usuario = usuario.find_one({'nombreUsuario': nombreUsuario})
	if(usuario):
		usuario['token']
	else:
		return False

def validarToken(nombreUsuario, contrasena, token):
	"""!@brief Desempaqueta el token y valida los campos.
	Devuelve true o false.
	
	@param nombreUsuario Nombre del usuario.
	@param contrasena Contrasena del usuario hasheada.
	@param token token a guardar.
	"""

	try:
		payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
		if(payload['nombreUsuario'] == nombreUsuario and payload['contrasena'] == contrasena):
			return True;
		else:
			return False;

	except jwt.ExpiredSignatureError:
		return False
	except jwt.InvalidTokenError:
		return False

