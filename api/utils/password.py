from argon2 import PasswordHasher

ph = PasswordHasher()


def password_hash(password: str):
    return ph.hash(password)


def password_verify(hashed_password: str, password: str):
    try:
        ph.verify(hashed_password, password)
        return True
    except:
        return False
    