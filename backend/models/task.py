import enum
from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship

from . import Base, Mapped, mapped_column, String, DateTime, Enum
from .project import Project

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
    
    project: Mapped['Project'] = relationship(back_populates="tasks")

    def __init__(self, id: str, name: str, description: str, code: str):
        self.id = id
        self.name = name
        self.description = description
        self.code = code