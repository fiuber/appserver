from mock import patch, MagicMock, PropertyMock
import unittest
import jwt

from src.models.token import Token
from src import mongo

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

	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenValido(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.return_value = {"nombreUsuario": "Mario", "contrasena": "Mario1234"}
		mockJWT.encode.return_value = "jkbdsgafgklfgk"

		mockFind = MagicMock()
		mockFind.find_one.return_value = {"token": "jdsjgjjkgfgjf"}

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		self.assertNotEqual(autenticador.obtenerToken(123, "driver","Mario","Mario1234"),False)
	
	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenExpirado(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.side_effect = tirarExcepcion
		mockJWT.encode.return_value = "ksdhkdghfhfgukfd"

		mockFind = MagicMock()
		mockFind.find_one.return_value = {"token": "jdsjgjjkgfgjf"}

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		self.assertNotEqual(autenticador.obtenerToken(123, "driver","Mario","Mario1234"),False)

	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenValidoDatosMal(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.return_value = {"nombreUsuario" : "Nicolas", "contrasena": "TuVieja"}
		mockJWT.encode.side_effect = "jkbsdfbgdsfbjkdsjbksdgjhd"

		mockFind = MagicMock()
		mockFind.find_one.return_value = {"token": "jdsjgjjkgfgjf"}

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		self.assertNotEqual(autenticador.obtenerToken(123, "driver","Mario","Mario1234"),False)

	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenExpiradoMalEncodeado(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.side_effect = tirarExcepcion
		mockJWT.encode.side_effect = tirarExcepcion

		mockFind = MagicMock()
		mockFind.find_one.return_value = {"token": "jdsjgjjkgfgjf"}

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		self.assertEqual(autenticador.obtenerToken(123, "driver","Mario","Mario1234"),False)

	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenNoExistenteEnMongo(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.side_effect = tirarExcepcion
		mockJWT.encode.return_value = "jkbdfjkdfjkbdfsjkdjkgg"

		mockFind = MagicMock()
		mockFind.find_one.return_value = False

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		self.assertNotEqual(autenticador.obtenerToken(123, "driver","Mario","Mario1234"),False)

	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenNoSePuedeRecuperarDeMongo(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.side_effect = tirarExcepcion
		mockJWT.encode.side_effect = "jkbdfjkdfjkbdfsjkdjkgg"

		mockFind = MagicMock()
		mockFind.find_one.side_effect = tirarExcepcion

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		self.assertNotEqual(autenticador.obtenerToken(123, "passenger","Mario","Mario1234"),False)

	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenDriverNoSePuedeRecuperarDeMongo(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.side_effect = tirarExcepcion
		mockJWT.encode.side_effect = "jkbdfjkdfjkbdfsjkdjkgg"

		mockFind = MagicMock()
		mockFind.find_one.return_value = {}

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).conductores = p 

		self.assertNotEqual(autenticador.obtenerToken(123, "driver","Mario","Mario1234"),False)

	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenNoSePuedeAlmacenarDeMongo(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.return_value = True
		mockJWT.encode.return_value = "jkbdfjkdfjkbdfsjkdjkgg"

		mockFind = MagicMock()
		mockFind.update.side_effect = tirarExcepcion

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		self.assertEqual(autenticador.obtenerToken(123, "driver","Mario","Mario1234"),False)

	@patch("src.models.token.jwt")
	@patch("src.models.token.mongo")
	def test_obtenerToken_tokenNoSePuedeAlmacenarDeMongo(self, mockPyMongo, mockJWT):
		autenticador = Token()

		mockJWT.decode.return_value = True
		mockJWT.encode.return_value = "jkbdfjkdfjkbdfsjkdjkgg"

		mockFind = MagicMock()
		mockFind.update.side_effect = tirarExcepcion

		p = PropertyMock(return_value = mockFind)
		type(mockPyMongo.db).usuarios = p  	
		
		self.assertEqual(autenticador.obtenerToken(123, "passenger","Mario","Mario1234"),False)
