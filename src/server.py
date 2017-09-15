import logging
from os import environ

from flask import Flask
from src import funcionesRdm
from src.views import index
from logging.config import fileConfig
from flask_pymongo import PyMongo

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

@app.route('/token')
def autenticar():
	return "{\"token\": \"jhgdfsghdsfagHGF342fdTrftyIUU786453\" }"

if __name__ == '__main__':
	port = os.environ.get('PORT', 5000)
	app.run(host='0.0.0.0', port=port)
