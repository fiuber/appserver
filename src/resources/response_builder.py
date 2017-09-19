from flask import jsonify, make_response

class ResponseBuilder:
	"""!@brief Clase para creacion de responses.

	Para ver creacion de errores: error_handler.ErrorHandler
		"""

	@staticmethod
	def build_response(response, status_code=200):
		"""!@brief Crea un Json con la respuesta.
			"""
		return make_response(jsonify(response), status_code)
