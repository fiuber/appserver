from flask import jsonify, make_response


class ErrorHandler:
  """!@brief Clase para creacion de errores. 

  Para ver creacion de respuestas correctas: response_builder.ResponseBuilder
    """

  @staticmethod
  def create_error_response(status_code, message):
    """!@brief Crea un Json con el codigo y el mensaje de error.
    """
    return make_response(
      jsonify(
            {
              "status_code": status_code,
              "message": message
            }
      ),
      status_code
    )