from datetime import datetime
from pydantic import BaseModel

from models.project import TaskStatus

class UserCreatePayload(BaseModel):
    username: str
    email: str
    password: str

class UserLoginPayload(BaseModel):
    email: str
    password: str

class CreateProjectPayload(BaseModel):
    name: str
    description: str = ""
    deadline: datetime

class CreateTaskPayload(BaseModel):
    name: str
    description: str = ""
    assignee: str
    status: TaskStatus

class EditTaskPayload(BaseModel):
    name: str = ""
    description: str = ""

class ChangeStatusPayload(BaseModel):
    status: TaskStatus

class ChangeAssigneePayload(BaseModel):
    assignee: str