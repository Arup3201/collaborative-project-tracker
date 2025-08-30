from pydantic import BaseModel

class UserCreatePayload(BaseModel):
    username: str
    email: str
    password: str