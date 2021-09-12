import hashlib


def to_hashcode(value, salt) -> str:
    return hashlib.sha512(str.encode(str(salt) + str(value))).hexdigest()
