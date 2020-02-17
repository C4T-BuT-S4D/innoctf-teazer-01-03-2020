from pyramid.view import view_config

from .middleware import login_required, with_user_response
from .models import User, Password
from .request import redirect


@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    if request.method == 'GET':
        return {}

    user = User.from_form(request)
    if not user:
        return {'error': 'invalid data'}

    session = user.login()

    response = redirect(request, '/')
    response.set_cookie('session', session)

    return response


@view_config(route_name='register', renderer='templates/register.jinja2')
def register(request):
    if request.method == 'GET':
        return {}

    user = User.from_form(request)
    if not user:
        return {'error': 'invalid data'}

    was_user = User.from_username(user.username)
    if was_user:
        return {'error': 'username taken'}

    user.register()

    return redirect(request, '/login/')


@view_config(route_name='logout')
def logout(request):
    user = User.from_request_session(request)
    if not user:
        return redirect(request, '/')

    user.logout(request)
    return redirect(request, '/')


@view_config(route_name='users', renderer='templates/users.jinja2')
@with_user_response
def list_users(_request):
    users = User.list()
    return {'users': users}


@view_config(route_name='user_profile', renderer='templates/user.jinja2')
@with_user_response
def get_user(request):
    username = request.matchdict.get('username')
    if not username:
        return redirect(request, '/')

    if request.method == 'GET':
        return {'username': username}

    user = User.from_username(username)
    if not user:
        return redirect(request, '/')

    password = request.POST.get('password')
    if not password:
        return {'error': 'invalid data', 'username': username}

    exists = Password.check(user.username, password)
    if exists:
        return {'passwords': Password.list(user.username), 'username': username}

    return {'error': 'invalid guess', 'username': username}


@view_config(route_name='add_password', renderer='templates/add_password.jinja2')
@login_required
@with_user_response
def add_password(request):
    if request.method == 'GET':
        return {}

    password = Password.from_form(request)
    if not password:
        return {'error': 'invalid data'}

    password.add()

    return redirect(request, f'/users/{password.user}/')


@view_config(route_name='home', renderer='templates/index.jinja2')
@with_user_response
def my_view(request):
    return {'project': 'passman'}
