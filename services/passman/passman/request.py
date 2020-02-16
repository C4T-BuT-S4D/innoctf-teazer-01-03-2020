from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound

from .models import User


class RequestUser:
    def __init__(self, request):
        self.request = request

    @reify
    def user(self):
        return User.from_request_session(self.request)


def build_redirect_url(request, path):
    return request.host_url + ':9171' + path


def redirect(request, path):
    return HTTPFound(build_redirect_url(request, path))
