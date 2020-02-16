from pyramid.config import Configurator

from .request import RequestUser


def register_routes(config):
    config.add_route('home', '/')
    config.add_route('login', '/login/')
    config.add_route('register', '/register/')
    config.add_route('logout', '/logout/')
    config.add_route('users', '/users/')
    config.add_route('user_profile', '/users/{username}/')
    config.add_route('add_password', '/add_password/')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_request_method(RequestUser, 'user', reify=True)

    register_routes(config)

    config.scan()
    return config.make_wsgi_app()
