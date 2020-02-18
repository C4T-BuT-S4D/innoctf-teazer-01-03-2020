from functools import wraps

from .models import User
from .request import redirect


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = User.from_request_session(request)
        if not user:
            return redirect(request, '/login/')
        return func(request, *args, **kwargs)

    return wrapper


def with_user_response(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, dict):
            user = User.from_request_session(request)
            if user:
                response['user'] = user
        return response

    return wrapper
