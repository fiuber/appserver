# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import Flask, request
from flask_pymongo import PyMongo

class User(object):
	"""docstring for User"""
	
	def __init__(self, id, tipo, usr, pwd, fb, name, lastname, email, birthdate):
		super(User, self).__init__()
		self.userId = id
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

	def exists_by_id(self):
		return True

	def stored_user_in_shared_server(self):
		return "5" # debe devolver el id

	def	modify_user_in_shared_server(self):
		return "ok"