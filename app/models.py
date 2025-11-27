from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, text, ForeignKey

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

    keys : Mapped[List["APIkey"]] = relationship(back_populates="user", lazy="selectin", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, username='{self.username}', rank='{self.rank}'), is_active:{self.is_active}>"
    
class APIkey(Base):
    __tablename__ = "apikeys"
    key_id : Mapped[int]  = mapped_column(Integer, primary_key=True)
    key : Mapped[str] = mapped_column(String(100), index=True)
    label: Mapped[str] = mapped_column(String(50))
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

    user: Mapped["User"] = relationship(back_populates="keys")

    def __repr__(self) -> str:
        return f"<APIKey(id={self.key_id}, name='{self.label}', user_id={self.user_id})>"