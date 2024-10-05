import hashlib


def md5(string: str) -> str:
    return hashlib.md5(string.encode('utf-8')).hexdigest()
