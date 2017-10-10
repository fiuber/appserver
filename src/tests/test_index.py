# -*- coding: utf-8 -*-
from resources.index import HelloWorld


def test_HelloWorld_devuelve_msje():
	service = HelloWorld()
	assert service.get() == '<h1><center> Bienvenido! App Server está en ejecución!</center></h1>'