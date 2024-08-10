from rest_framework.exceptions import APIException

class TaskNotFoundException(APIException):
    status_code = 404
    default_detail = 'The requested task does not exist.'
    default_code = 'task_not_found'

class BadRequestException(APIException):
    status_code = 400
    default_detail = 'Bad Request.'
    default_code = 'bad_request'