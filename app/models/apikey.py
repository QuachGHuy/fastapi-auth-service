from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, text, ForeignKey

from app.db.base import Base

class APIKey(Base):
    __tablename__ = "apikeys"
    key_id : Mapped[int]  = mapped_column(Integer, primary_key=True)
    key : Mapped[str] = mapped_column(String(100), index=True)
    label: Mapped[str] = mapped_column(String(50))
    description : Mapped[str] = mapped_column(String(150), nullable=True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

    user: Mapped["User"] = relationship(back_populates="keys")

    def __repr__(self) -> str:
        return f"<APIKey(id={self.key_id}, label='{self.label}', user_id={self.user_id})>"