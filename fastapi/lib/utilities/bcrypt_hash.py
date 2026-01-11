import bcrypt


class BcryptHash():
    def bcrypt_hash(self, plain_password: str) -> str:
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        return hashed.decode()

    def bcrypt_verify(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
