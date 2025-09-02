class BadPayloadError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DBOverloadError(Exception):
    def __init__(self):
        super().__init__("Too many clients trying to connect with server")

class DBIntegrityError(Exception):
    def __init__(self):
        super().__init__("Database integrity violated")

class NotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class IncorrectPasswordError(Exception):
    def __init__(self):
        super().__init__("user has put wrong password")

class JWTError(Exception):
    def __init__(self, message: str):
        super().__init__(message)