import logging
from flask import request

from os import environ


from urllib import unquote
from flask import json
from flask import Flask, request
from flask_restful import Resource, Api
from logging.config import fileConfig
from flask_pymongo import PyMongo


from resources.index import HelloWorld
from resources.auth import Auth

app = Flask(__name__)
api = Api(app)
app.config['MONGO_DBNAME'] = 'fiuberappserver'
app.config['MONGO_URI'] = 'mongodb://fiuberappserver:fiuberappserver@ds123534.mlab.com:23534/fiuberappserver'
mongo = PyMongo(app)


api.add_resource(HelloWorld, '/')
api.add_resource(Auth, '/token')

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


if __name__ == '__main__':
	port = os.environ.get('PORT', 5000)
	app.run(host='0.0.0.0', port=port)
