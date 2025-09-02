import bcrypt, re
from sqlalchemy.exc import OperationalError

from models.user import User
from db import Database
from utils.id import generate_id
from exceptions import BadPayloadError, NotFoundError, DBOverloadError, AlreadyExistError
from exceptions.auth import IncorrectPasswordError

class AuthService:
    def __init__(self):
        self.session = Database().get_session()

    def register(self, username: str, email: str, password: str):
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            raise BadPayloadError("'email' field value is not a valid email")

        with self.session() as session:
            user = session.query(User).filter(User.email==email).first()
            if user:
                raise AlreadyExistError(f"User with email {email} already exist")

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User(generate_id('USER_'), username, email, password_hash.decode('utf-8'))
        
        try:
            with self.session() as session:
                session.add(user)
                session.commit()
        except OperationalError as e:
            print(e)
            raise DBOverloadError()

    def login(self, email: str, password: str):
        try:
            with self.session() as session:
                user = session.query(User).filter(User.email==email).first()
                
                if not user:
                    raise NotFoundError(f"User with email {email} does not exist")
                
                if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                    raise IncorrectPasswordError()
                
                return {
                    "id": user.id, 
                    "email": user.email, 
                    "name": user.name,
                    "created_at": user.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
        except OperationalError as e:
            print(e)
            raise DBOverloadError()