import logging
from flask import request

from os import environ

from flask import Flask
from src import funcionesRdm
from src import auth
from src.views import index
from logging.config import fileConfig
from flask_pymongo import PyMongo

from urllib import unquote
from flask import json

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'fiuberappserver'
app.config['MONGO_URI'] = 'mongodb://fiuberappserver:fiuberappserver@ds123534.mlab.com:23534/fiuberappserver'
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return index.mensajeCorriendo()

@app.route('/bienvenido')
def dar_bievenida():
	return 'Bienvenido, 2 + 2 es: ' + str(funcionesRdm.sumar(2,2))

@app.route('/log')
def probarLog():
	"""Un comentario"""
	log = mongo.db.log
	log.insert({"Tipo": "Warning", "Mensaje": "No anda el log"})
	resultados = log.find({})
	mostrar = ""
	for documento in resultados:
          mostrar += str(documento)+"<br>"
	return mostrar

@app.route('/dbtest')
def probarDB():
	usuarios = mongo.db.usuarios
	usuarios.insert({"Nombre" : "Yo", "Apellido": "Bebopipi"})
	resultados = usuarios.find({})
	mostrar = ""
	for documento in resultados:
          mostrar += str(documento)+"<br>"
	return mostrar

@app.route('/token', methods=['POST'])
def autenticar():
	"""!@brief Autentica al usuario una unica vez."""

	"""Si no se recibieron los datos todo mal."""	
	datos = request.get_json(silent=True);
	if(not datos):
		return "Cagaste", 404

	"""Se validan que esten todos los datos necesarios."""
	nombreUsuario =  datos['nombreUsuario']
	contrasena =  datos['contrasena']

	if(not nombreUsuario or not contrasena):
		return "Cagaste", 404

	token = auth.recuperarToken(nombreUsuario);

	"""Si no esta el token puede ser que no este autenticado todavia."""
	if(not token):
		"""
			Pegarle al server para ver si existe el usuario y si existe crearle un token y agregarlo
		"""
		existe = True;

		if(not existe):
			return "Cagaste", 404
	
		token = auth.generarToken(nombreUsuario, contrasena)
		if(not token):
			return "Cagaste", 404

		"""Si no se puede almacenar no tiene sentido seguir aunque el token se haya generado"""
		if(not almacenarToken(nombreUsuario, token)):
			return "Cagaste", 404
		return token
	
	"""Si es valido se le envia y sino error."""
	autentico = auth.validarToken(nombreUsuario, contrasena, token)
	if(not autentico):
		return "Cagaste", 404

	return token

if __name__ == '__main__':
	port = os.environ.get('PORT', 5000)
	app.run(host='0.0.0.0', port=port)
