from flask import request
from os import environ

from urllib import unquote
from flask import json
from flask import Flask, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

app = Flask(__name__)
api = Api(app)
app.config['MONGO_DBNAME'] = 'fiuberappserver'		
app.config['MONGO_URI'] = 'mongodb://fiuberappserver:fiuberappserver@ds123534.mlab.com:23534/fiuberappserver'		
mongo = PyMongo(app)
directionsAPIKey = "AIzaSyDvms5q5db1RR0P6d1-lwkO9lEJy_Tv_1U"
URLSharedServer = "http://fiuber-shared.herokuapp.com"
