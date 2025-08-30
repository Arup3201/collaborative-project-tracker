from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Env

class Database:
    def __init__(self):
        engine_string = f"postgresql+psycopg2://{Env.DB_USER}:{Env.DB_PASS}@{Env.DB_HOST}:{Env.DB_PORT}/${Env.DB_NAME}"
        self.engine = create_engine(engine_string)
    
    def get_session(self):
        session = sessionmaker(self.engine)
        return session