from src import app, api
from coverage import coverage
from mock import patch, MagicMock, PropertyMock
import unittest




cov = coverage(branch=True, omit=["src/tests/*", "/usr/local/lib/*", "src/server.py", "src/resources/__init__.py", "src/__init__.py", "src/models/__init__.py", "src/resources/index.py"])
cov.start()

from src.tests.test_endpoint_agregarAutoUsuario import TestEndpointAgregarAutoUsuario
from src.tests.test_token import TestToken
from src.tests.test_conectividad import TestConectividad
from src.tests.test_push import TestPush
from src.tests.test_log import TestLog
from src.tests.test_endpoint_token import TestEndpointToken
from src.tests.test_endpoint_modificarAutoUsuario import TestEndpointModificarAutoUsuario
from src.tests.test_endpoint_eliminarAutoUsuario import TestEndpointEliminarAutoUsuario
from src.tests.test_endpoint_autoPorID import TestEndpointAutoPorID
from src.tests.test_endpoint_autosPorUsuario import TestEndpointAutosPorUsuario
from src.tests.test_endpoint_autosPorPosicionCercana import TestEndpointAutosPorPosicionCercana
from src.tests.test_endpoint_aceptarViaje import TestEndpointAceptarViaje
from src.tests.test_endpoint_agregarPosibleViaje import TestEndpointAgregarPosibleViaje
from src.tests.test_endpoint_obtenerPosiblesViajes import TestEndpointObtenerPosiblesViajes
from src.tests.test_endpoint_agregarUsuario import TestEndpointAgregarUsuario
from src.tests.test_endpoint_modificarUsuario import TestEndpointModificarUsuario
from src.tests.test_endpoint_eliminarUsuario import TestEndpointEliminarUsuario
from src.tests.test_endpoint_driverModificarPosicion import TestEndpointDriverModificarPosicion
from src.tests.test_endpoint_usuarioModificarPosicion import TestEndpointUsuarioModificarPosicion
from src.tests.test_endpoint_modificarMetodopago import TestEndpointModificarMetodopago
from src.tests.test_endpoint_obtenerMetodopago import TestEndpointObtenerMetodopago
from src.tests.test_endpoint_rechazarViaje import TestEndpointRechazarViaje
from src.tests.test_endpoint_eliminarMetodopago import TestEndpointEliminarMetodopago
from src.tests.test_endpoint_rutaEntrePuntos import TestEndpointRutaEntrePuntos

if __name__ == '__main__':
	try:
		unittest.main()
	except:
		pass
	cov.stop()
	cov.save()
	print("\n\nCoverage Report:\n")
	cov.report()
        cov.html_report(directory='tmp/coverage')
	cov.erase()
