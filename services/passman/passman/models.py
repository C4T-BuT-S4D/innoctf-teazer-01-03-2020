import secrets
from typing import List

from .storage import get_db


class User:
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
        }

    def save(self):
        db = get_db()
        h = db.Hash(f'user:{self.username}')
        h.update(**self.to_dict())

    def register(self):
        self.save()

        db = get_db()
        users = db.List('users')
        users.prepend(self.username)

    def login(self):
        session = secrets.token_hex(20)

        db = get_db()
        h = db.Hash(f'session:{session}')
        h.update(**self.to_dict())

        return session

    @staticmethod
    def logout(request):
        if 'session' not in request.cookies:
            return

        db = get_db()
        db.delete(f'session:{request.cookies["session"]}')

    @staticmethod
    def list():
        db = get_db()
        users = db.List('users')
        return users.as_list(decode=True)

    @classmethod
    def from_dict(cls, d):
        if 'username' not in d or 'password' not in d:
            return None
        return cls(**d)

    @classmethod
    def from_form(cls, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return None

        return cls(username=username, password=password)

    @classmethod
    def from_request_session(cls, request):
        session = request.cookies.get('session')
        if not session:
            return None

        db = get_db()
        h = db.Hash(f'session:{session}')
        return cls.from_dict(h.as_dict(decode=True))

    @classmethod
    def from_username(cls, username):
        db = get_db()
        h = db.Hash(f'user:{username}')
        return cls.from_dict(h.as_dict(decode=True))


class Password:
    user: str
    password: str

    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password

    def add(self):
        db = get_db()
        passwords = db.List(f'user:{self.user}:passwords')
        passwords.prepend(self.password)

        bf = db.bloom_filter(f'user:{self.user}:bf', size=4)
        bf.add(self.password)

    @staticmethod
    def list(user: str) -> List[str]:
        db = get_db()
        passwords = db.List(f'user:{user}:passwords')
        return passwords.as_list(decode=True)

    @staticmethod
    def check(user: str, password: str) -> bool:
        db = get_db()
        bf = db.bloom_filter(f'user:{user}:bf', size=4)
        return bf.contains(password)

    @classmethod
    def from_form(cls, request):
        if 'password' not in request.POST:
            return None

        user = User.from_request_session(request)
        return cls(user=user.username, password=request.POST['password'])
