from models import Base, User, Project, Task, Membership

from env import load_dotenv
load_dotenv()

from db import Database

database = Database()
Base.metadata.create_all(database.engine)