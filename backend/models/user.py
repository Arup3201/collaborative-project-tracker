from datetime import datetime, timezone

from models import Base, Mapped, mapped_column, String, DateTime


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String(150), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    def __init__(self, id, name, email, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now(tz=timezone.utc)
