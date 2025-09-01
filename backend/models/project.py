from typing import List
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import relationship

from . import Base, Mapped, mapped_column, String, DateTime
from .task import Task

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(150), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    code: Mapped[str] = mapped_column(String, nullable=False)
    
    tasks: Mapped[List['Task']] = relationship(back_populates="project")

    def __init__(self, id: str, name: str, description: str, code: str):
        self.id = id
        self.name = name
        self.description = description
        self.code = code