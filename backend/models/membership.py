import enum
from datetime import datetime
from sqlalchemy import func, ForeignKey

from models import Base, Mapped, mapped_column, DateTime, Enum, String

class Role(enum.Enum):
    Member = "Member"
    Owner = "Owner"

class Membership(Base):
    __tablename__ = "memberships"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    role: Mapped[Role] = mapped_column(Enum(Role))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __init__(self, user_id: str, project_id: str):
        self.user_id = user_id
        self.project_id = project_id
