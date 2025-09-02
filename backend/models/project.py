import enum
from typing import List
from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship

from models import Base, Mapped, mapped_column, String, DateTime, Enum
from models import Membership

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(150), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    code: Mapped[str] = mapped_column(String, nullable=False)
    
    tasks: Mapped[List['Task']] = relationship(back_populates="project")
    memberships: Mapped[List['Membership']] = relationship(cascade="all, delete-orphan")

    def __init__(self, id: str, name: str, description: str, deadline: datetime, code: str):
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.code = code

class TaskStatus(enum.Enum):
    ToDo = "To Do"
    InProgress = "In Progress"
    Completed = "Completed"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(150), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    assignee: Mapped[str] = mapped_column(ForeignKey("users.id"))
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus))
    
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    project: Mapped['Project'] = relationship(back_populates="tasks")

    def __init__(self, id: str, name: str, description: str, assignee: str, status: TaskStatus):
        self.id = id
        self.name = name
        self.description = description
        self.assignee = assignee
        self.status = status