from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime