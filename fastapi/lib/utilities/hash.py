import bcrypt


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode(), salt)
    return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    hashed = plain_password.encode()
    return bcrypt.checkpw(hashed, hashed_password.encode())
