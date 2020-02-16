import re

import requests
from checklib import *

PORT = 9171


class CheckMachine:
    def __init__(self, checker: BaseChecker):
        self.c = checker

    @property
    def url(self):
        return f'http://{self.c.host}:{PORT}'

    def register(self, username=None, password=None):
        username = username or rnd_username()
        password = password or rnd_password()
        r = requests.post(f'{self.url}/register/', data={'username': username, 'password': password})
        self.c.check_response(r, 'Could not register')
        self.c.assert_in('login', r.url, 'Invalid page after register')
        return username, password

    def login(self, username, password):
        sess = get_initialized_session()
        r = sess.post(f'{self.url}/login/', data={'username': username, 'password': password})
        self.c.check_response(r, 'Could not login')

        data = self.c.get_text(r, 'Could not login')
        self.c.assert_in(username, data, 'Invalid page after login')
        return sess

    def list_users(self, sess):
        r = sess.get(f'{self.url}/users/')
        self.c.check_response(r, 'Could not list users')
        return self.c.get_text(r, 'Could not list users')

    def add_password(self, sess, password=None):
        password = password or rnd_password()
        r = sess.post(f'{self.url}/add_password/', data={'password': password})
        self.c.check_response(r, 'Could not add password')
        self.c.assert_in('users', r.url, 'Invalid page after password')

        return password

    def list_passwords(self, sess, username, password):
        r = sess.get(f'{self.url}/users/{username}/')
        self.c.check_response(r, 'Could not get user profile')
        data = self.c.get_text(r, 'Could not get user profile')
        self.c.assert_in(username, data, 'Could not get user profile')

        r = sess.post(f'{self.url}/users/{username}/', data={'password': password})
        self.c.check_response(r, 'Could not get user passwords')
        data = self.c.get_text(r, 'Could not get user passwords')
        self.c.assert_in(username, data, 'Could not get user passwords')
        self.c.assert_in(password, data, 'Could not get user passwords')

        return re.findall(r'<li class="list-group-item">(\S*)</li>', data)
