from typing import List
from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import relationship

from models import Base, Mapped, mapped_column, String, DateTime
from models import Membership

class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String(150), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    memberships: Mapped[List['Membership']] = relationship(cascade="all, delete-orphan")

    def __init__(self, id, name, email, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now(tz=timezone.utc)
