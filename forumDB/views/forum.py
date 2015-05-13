from forumDB.functions.common import make_required, make_optional, response, RequestError, ResponseCodes
from forumDB.functions.forum.forum_functions import create_forum
from forumDB.functions.forum.getters import get_list_threads, get_list_posts, get_forum_details
from forumDB.functions.user.getters import get_forum_user_list

def create(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['name', 'short_name', 'user'])
            response_data = create_forum(required_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def details(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['forum'])
            optional = make_optional("GET", request, ['related'])
            response_data = get_forum_details(required_params['forum'], optional['related'], None)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def list_threads(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['forum'])
            optional_parameters1 = make_optional("GET", request, ['since', 'limit', 'order'])
            optional_parameters2 = make_optional("GET", request, ['related'], array=True)
            optional_parameters = optional_parameters1.copy()
            optional_parameters.update(optional_parameters2)
            response_data = get_list_threads(required_params, optional_parameters)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def list_posts(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['forum'])
            optional_parameters1 = make_optional("GET", request, ['since', 'limit', 'order'])
            optional_parameters2 = make_optional("GET", request, ['related'], array=True)
            optional_parameters = optional_parameters1.copy()
            optional_parameters.update(optional_parameters2)
            response_data = get_list_posts(required_params['forum'], optional_parameters)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def list_users(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['forum'])
            optional_params = make_optional("GET", request, ['since_id', 'limit', 'order'])
            response_data = get_forum_user_list(required_params, optional_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)