from mock import patch, MagicMock, PropertyMock
import unittest
import jwt

from src.models.conectividad import Conectividad

def tirarExcepcion():
	raise Exception("Mal")


class TestConectividad(unittest.TestCase):
	
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_post200OK(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.post.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertNotEqual(conectividad.post("users", {"Hola": "Chau"}, {"Hola": "Chau"}),False)

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_post200MalJSON(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.post.return_value = MockAux
		mockJson.loads.side_effect = tirarExcepcion;
		
		self.assertFalse(conectividad.post("users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_postNo200(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.post.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.post("users", {"Hola": "Chau"}, {"Hola": "Chau"}))




	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_get200OK(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.get.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertNotEqual(conectividad.get("users", {"Hola": "Chau"}),False)

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_get200MalJSON(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.get.return_value = MockAux
		mockJson.loads.side_effect = tirarExcepcion;
		
		self.assertFalse(conectividad.get("users", {"Hola": "Chau"}))

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_getNo200(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.get.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.get("users", {"Hola": "Chau"}))

	

	
	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_put200OK(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.put.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertNotEqual(conectividad.put("users", {"Hola": "Chau"}, {"Hola": "Chau"}),False)

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_put200MalJSON(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.put.return_value = MockAux
		mockJson.loads.side_effect = tirarExcepcion;
		
		self.assertFalse(conectividad.put("users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_putNo200(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.put.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.put("users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_delete200OK(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.delete.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertNotEqual(conectividad.delete("users", {"Hola": "Chau"}, {"Hola": "Chau"}),False)

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_delete200MalJSON(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 200)
		type(MockAux).status_code = p  

		mockRequest.delete.return_value = MockAux
		mockJson.loads.side_effect = tirarExcepcion;
		
		self.assertFalse(conectividad.delete("users", {"Hola": "Chau"}, {"Hola": "Chau"}))

	@patch("src.models.conectividad.requests")
	@patch("src.models.conectividad.json")
	def test_deleteNo200(self, mockJson, mockRequest):
		conectividad = Conectividad("www.llallala.com","kdsfjk8sdgkgkfg")

		MockAux = MagicMock()
		p = PropertyMock(return_value = 400)
		type(MockAux).status_code = p  

		mockRequest.delete.return_value = MockAux
		mockJson.loads.return_value = {"OKOKOO"}
		
		self.assertFalse(conectividad.delete("users", {"Hola": "Chau"}, {"Hola": "Chau"}))
