# -*- coding: utf-8 -*-
import index


def test_mensajeCorriendo_devuelve_msje():
    assert index.mensajeCorriendo() == '<h1><center> Bienvenido! App Server está en ejecución!</center></h1>'