import bcrypt

from models.user import User
from db import Database
from utils.id import generate_id

class AuthService:
    def __init__(self):
        self.session = Database().get_session()

    def register(self, username: str, email: str, password: str):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User(generate_id('USER_'), username, email, password_hash.decode('utf-8'))
        
        with self.session() as session:
            session.add(user)
            session.commit()

    def login(self, email: str, password: str):
        with self.session() as session:
            user = session.query(User).filter(User.email==email).first()
            
            if not user:
                raise ValueError("email not found")
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                raise ValueError("password mismatch")
            
            return {
                "id": user.id, 
                "email": user.email, 
                "name": user.name,
                "created_at": user.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
            }