class BadPayloadError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DBError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class NotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class IncorrectPasswordError(Exception):
    def __init__(self):
        super().__init__("user has put wrong password")

class JWTError(Exception):
    def __init__(self, message: str):
        super().__init__(message)