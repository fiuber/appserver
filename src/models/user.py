# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo

from conectividad import Conectividad 

class User(object):
	"""docstring for User"""
	
	def __init__(self, tipo, usr, pwd, fb, name, lastname, email, birthdate):
		super(User, self).__init__()
		self.tipo = tipo
		self.usr = usr
		self.pwd = pwd
		self.fb = fb
		self.name = name
		self.lastname = lastname
		self.email = email
		self.birthdate = birthdate


	def exists_by_username(self):
		return False

	def stored_user_in_shared_server(self):
		return "ok" # debe devolver el id

	def	modify_user_in_shared_server(self):
		return "ok"