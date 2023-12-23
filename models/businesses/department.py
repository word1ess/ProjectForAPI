from datetime import datetime
from typing import List
from decimal import Decimal
from sqlalchemy import ForeignKey, DateTime, func, String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Department(Base):
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, unique=True)
    allocated_budget: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    budget: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    director_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    director: Mapped["User"] = relationship(back_populates="departments", lazy="selectin")

    business_id: Mapped[int] = mapped_column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"))
    business: Mapped["Business"] = relationship(back_populates="departments", lazy="selectin")

    expenses: Mapped[List["Expense"]] = relationship(back_populates="department", lazy="selectin",
                                                     cascade="all, delete-orphan")

    created_at = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
