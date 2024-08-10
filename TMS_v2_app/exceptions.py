from rest_framework.exceptions import APIException

class TaskNotFoundException(APIException):
    status_code = 404
    default_detail = 'Task not found.'
    default_code = 'task_not_found'