import random
import hashlib


def secure_generate_password():
    return "".join(["{}".format(random.randint(0, 9)) for _ in range(0, 10)])


def secure_hash_password(password: str):
    return hashlib.sha1(password.encode()).hexdigest()


def compare_password(hpassw: str, password: str):
    return hpassw == secure_hash_password(password)
