from mock import patch, MagicMock, PropertyMock
import unittest
import jwt

from src.models.conectividad import Conectividad

def tirarExcepcion():
	raise Exception("Mal")

def log():
	return True

def time():
	if(time.contador == 0):
		time.contador += 1
		return 0
	else:
		return 10000000
time.contador = 0
	  


class TestConectividad(unittest.TestCase):

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_post200OK(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()

		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.post.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertNotEqual(conectividad.post("http://www.google.com.ar","users", {"Hola": "Chau"}, {"Hola": "Chau"}, {"content-type": "application/json"}),False)

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_postMalJSON(self, mockJson, mockRequest, mockLog):
		mockLog.side_effect = log
		conectividad = Conectividad()

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.post.return_value = MockAux
		mockJson.loads.side_effect = tirarExcepcion;
		
		self.assertTrue(conectividad.post("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_postNo200(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.post.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.post("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}))



	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_get200OK(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.get.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertNotEqual(conectividad.get("http://www.google.com.ar", "users", {"Hola": "Chau"}),False)

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_getMalJSON(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.get.return_value = MockAux
		mockJson.loads.side_effect = tirarExcepcion;
		
		self.assertTrue(conectividad.get("http://www.google.com.ar", "users", {"Hola": "Chau"}))

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_getNo200(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.get.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.get("http://www.google.com.ar", "users", {"Hola": "Chau"}))

	

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_put200OK(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 204)
		type(MockAux).status_code = p  

		mockRequest.put.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertNotEqual(conectividad.put("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}),False)

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_putMalJSON(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.put.return_value = MockAux
		mockJson.loads.side_effect = tirarExcepcion;
		
		self.assertTrue(conectividad.put("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_putNo200(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.put.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.put("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_delete200OK(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.delete.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertNotEqual(conectividad.delete("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}),False)

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_deleteNo200(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.delete.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.delete("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_delete200MalJSON(self, mockJson, mockRequest, mockLog):
		conectividad = Conectividad()
		mockLog.side_effect = log

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.delete.return_value = MockAux
		mockJson.loads.side_effect = tirarExcepcion;
		
		self.assertTrue(conectividad.delete("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.mongo")
	@patch("src.models.conectividad.time")
	@patch("src.models.conectividad.Log")
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_deleteNo200TokenRenovado(self, mockJson, mockRequest, mockLog, mockTime, mockMongo):
		conectividad = Conectividad()

		mockPost = True
		mockMongo = True
		mockLog.return_value = True
		mockTime.time.side_effect = time

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.delete.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.delete("http://www.google.com.ar", "users", {"Hola": "Chau"}, {"Hola": "Chau"}))

