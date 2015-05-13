from forumDB.functions.common import make_required, make_optional, response, RequestError, ResponseCodes
from forumDB.functions.post.getters import get_post_list
from forumDB.functions.thread.getters import get_list
from forumDB.functions.thread.thread_functions import close_or_open, thread_vote, get_thread_details, unsubscribe_thread, subscribe_thread, create_thread, thread_update, thread_remove_restore

def create(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request,
                                            ['forum', 'title', 'isClosed', 'user', 'date', 'message', 'slug'])
            optional_params = make_optional("POST", request, ['isDeleted'])
            response_data = create_thread(required_params, optional_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def subscribe(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['user', 'thread'])
            response_data = subscribe_thread(required_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def unsubscribe(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['user', 'thread'])
            response_data = unsubscribe_thread(required_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def details(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['thread'])
            optional_params = make_optional("GET", request, ['related'], array=True)
            response_data = get_thread_details(required_params['thread'], optional_params['related'], None)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def vote(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['vote', 'thread'])
            response_data = thread_vote(required_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def open(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['thread'])
            response_data = close_or_open('open', required_params['thread'])
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def close(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['thread'])
            response_data = close_or_open('close', required_params['thread'])
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def list(request):
    if request.method == 'GET':
        try:
            user = request.GET.get('user')
            forum = request.GET.get('forum')
            optional_parameters = make_optional("GET", request, ['since', 'limit', 'order'])
            response_data = []
            if user is None:
                if forum is None:
                    response_error('you should set "user" or "forum"')
                else:
                    response_data = get_list('forum', forum, optional_parameters)
            else:
                response_data = get_list('user', user, optional_parameters)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def update(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['message', 'thread', 'slug'])
            response_data = thread_update(required_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def list_posts(request):
    if request.method == 'GET':
        try:
            required_params = make_required("GET", request, ['thread'])
            optional_params = make_optional("GET", request, ['since', 'limit', 'order'])
            required_params['type'] = 'thread'
            response_data = get_post_list(required_params, optional_params)
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def remove(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['thread'])
            response_data = thread_remove_restore(required_params, 'remove')
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)


def restore(request):
    if request.method == 'POST':
        try:
            required_params = make_required("POST", request, ['thread'])
            response_data = thread_remove_restore(required_params, 'restore')
            return response(response_data)
        except RequestError as exception:
            return response(exception.message, exception.code)
    else:
        return response("Incorrect request type", ResponseCodes.BAD_REQUEST)