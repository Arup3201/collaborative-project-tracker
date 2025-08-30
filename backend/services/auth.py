import bcrypt

from models.user import User
from db import Database
from utils.id import generate_id

class AuthService:
    def __init__(self):
        pass

    def register(self, username: str, email: str, password: str):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User(generate_id('USER_'), username, email, password_hash)
        
        session = Database().get_session()
        with session() as session:
            session.add(user)
            session.commit()
