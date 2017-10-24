import logging
from flask import request

from os import environ

from urllib import unquote
from flask import json
from flask import Flask, request
from flask_restful import Resource, Api
from logging.config import fileConfig
from flask_pymongo import PyMongo

from src.models.conectividad import Conectividad
from src import api, app


from resources.index import HelloWorld
from resources.auth import Auth
from resources.userControl import Register, UserController
from resources.autoPorID import AutoPorID
from resources.autosPorUsuario import AutosPorUsuario
from resources.autosPorPosicionCercana import AutosPorPosicionCercana
from resources.agregarAutoUsuario import AgregarAutoUsuario
from resources.eliminarAutoUsuario import EliminarAutoUsuario
from resources.modificarAutoUsuario import ModificarAutoUsuario
from resources.driverModificarPosicion import DriverModificarPosicion



api.add_resource(HelloWorld, '/')
api.add_resource(Auth, '/token')
api.add_resource(Register, '/users')
api.add_resource(UserController, '/users/<userId>')
api.add_resource(AgregarAutoUsuario, '/driver/<IDUsuario>/cars')
api.add_resource(ModificarAutoUsuario, '/driver/<IDUsuario>/cars/<IDAuto>')
api.add_resource(EliminarAutoUsuario, '/driver/<IDUsuario>/cars/<IDAuto>')
api.add_resource(AutoPorID, '/driver/<IDUsuario>/cars/<IDAuto>')
api.add_resource(AutosPorUsuario, '/driver/<IDUsuario>/cars')
api.add_resource(DriverModificarPosicion, '/driver/<IDUsuario>/position')
api.add_resource(AutosPorPosicionCercana, '/driver/search')


if __name__ == '__main__':
	port = os.environ.get('PORT', 5000)
	app.run(host='0.0.0.0', port=port)
