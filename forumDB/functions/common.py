import json
from django.http import HttpResponse

def response(response_data, code=0):
    return HttpResponse(json.dumps({'code': code, 'response': response_data}), content_type='application/json')

class ResponseCodes:
    OK = 0
    NOT_FOUND = 1
    BAD_REQUEST = 2
    INVALID_REQUEST = 3
    UNKNOWN_ERROR = 4
    USER_EXISTS = 5

class RequestError(Exception):
    def __init__(self, message, code):
        super(RequestError, self).__init__(message)
        self.code = code

def make_optional(request_type, request, parameters, array=False):
    optional_parameters = {}
    if request_type == "POST":
        request_data = json.loads(request.body)
        for parameter in parameters:
            try:
                optional_parameters[parameter] = request_data[parameter].encode('utf-8')
            except KeyError:
                optional_parameters[parameter] = None
            except Exception:
                optional_parameters[parameter] = request_data[parameter]
    if request_type == "GET":
        for parameter in parameters:
            try:
                if (array):
                    optional_parameters[parameter] = [x.encode('utf-8') for x in request.GET.getlist(parameter)]
                else:
                    optional_parameters[parameter] = request.GET.get(parameter).encode('utf-8')
            except KeyError:
                optional_parameters[parameter] = None
            except Exception:
                optional_parameters[parameter] = request.GET.get('utf-8')

    return optional_parameters


def make_required(request_type, request, parameters):
    required_parameters = {}
    if request_type == "POST":
        request_data = json.loads(request.body)
        for parameter in parameters:
            try:
                required_parameters[parameter] = request_data[parameter].encode('utf-8')
            except KeyError:
                raise RequestError('Incorrect request.', 3)
            except Exception:
                required_parameters[parameter] = request_data[parameter]

    if request_type == "GET":
        for parameter in parameters:
            try:
                required_parameters[parameter] = request.GET.get(parameter).encode('utf-8')
            except Exception:
                required_parameters[parameter] = request.GET.get(parameter)
            if required_parameters[parameter] is None:
                raise RequestError('Incorrect request.', 3)
    return required_parameters