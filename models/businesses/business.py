from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, DateTime, func, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Business(Base):
    __tablename__ = 'businesses'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, unique=True)

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    owner: Mapped["User"] = relationship(back_populates="businesses", lazy="selectin")

    departments: Mapped[List["Department"]] = relationship(back_populates="business", lazy="selectin",
                                                           cascade="all, delete-orphan")

    created_at = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
