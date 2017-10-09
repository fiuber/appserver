from mock import patch, MagicMock
from nose.tools import assert_is_not_none
import unittest
import jwt

from src.models.token import Token

def tirarExcepcion():
	raise Exception("Token invalido")



class TestToken(unittest.TestCase):

	@patch("src.models.token.jwt")
	def test_validarToken_valido(self, claseMock):
		autenticador = Token()
		claseMock.decode.return_value = True
		
		self.assertTrue(autenticador.validarToken("jhsuiusdfui"))

	@patch("src.models.token.jwt")
	def test_validarToken_invalido(self, claseMock):
		autenticador = Token()
		claseMock.decode.side_effect = tirarExcepcion
		
		self.assertFalse(autenticador.validarToken("jhsuiusdfui"))


	
if __name__ == '__main__':
    unittest.main()
