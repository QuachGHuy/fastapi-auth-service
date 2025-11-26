from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean,text

from app.database import Base

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int]  = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    points: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    rank: Mapped[str] = mapped_column(String(20), server_default="Bronze")
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, username='{self.username}', rank='{self.rank}'), is_active:{self.is_active}>"