from walrus import Walrus

_db = None


def get_db():
    global _db
    if _db is None:
        _db = Walrus(host='redis', port=6379, db=1)
    return _db
