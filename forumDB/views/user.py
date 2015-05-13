from forumDB.functions.common import make_required, make_optional, response, RequestError, ResponseCodes
from forumDB.functions.database import exec_clear
from forumDB.functions.post.getters import get_post_list
from forumDB.functions.user.getters import get_list_followers2
from forumDB.functions.user.user_functions import *

def clear(request):
    if request.method == 'POST':
        try:
            exec_clear('TRUNCATE Users', [])
            exec_clear('TRUNCATE Forums', [])
            exec_clear('TRUNCATE Threads', [])
            exec_clear('TRUNCATE Posts', [])
            exec_clear('TRUNCATE Subscriptions', [])
            exec_clear('TRUNCATE Followers', [])
            return response(None)
        except Exception as exception:
            return response(exception.message, ResponseCodes.UNKNOWN_ERROR)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def create(request):
    if request.method == 'POST':
        try:
            optional_parameters = make_optional("POST", request, ['isAnonymous'])
            required_params = make_required("POST", request, ['email', 'name', 'username', 'about'])
            response_data = create_user(required_params, optional_parameters)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
        except Exception as exception:
            raise exception
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def follow(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['follower', 'followee'])
            response_data = save_follow(required_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def unfollow(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['follower', 'followee'])
            response_data = remove_follow(required_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def details(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['user'])
            response_data = get_user_details(required_params['user'], 'email', None)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def list_followers(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['user'])
            optional_parameters = make_optional("GET", request, ['limit', 'since_id', 'order'])
            required_params['type'] = 'follower'
            response_data = get_list_followers2(required_params, optional_parameters)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def list_following(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['user'])
            optional_parameters = make_optional("GET", request, ['limit', 'since_id', 'order'])
            required_params['type'] = 'followee'
            response_data = get_list_followers2(required_params, optional_parameters)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def update(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['user', 'name', 'about'])
            response_data = update_user(required_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def list_posts(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['user'])
            optional_params = make_optional("GET", request, ['since', 'limit', 'order'])
            required_params['type'] = 'user'
            response_data = get_post_list(required_params, optional_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)