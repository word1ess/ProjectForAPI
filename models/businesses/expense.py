from datetime import datetime
from decimal import Decimal
from sqlalchemy import ForeignKey, DateTime, func, String, Integer, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Expense(Base):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    expense_date = mapped_column(Date, default=datetime.now)

    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    creator: Mapped["User"] = relationship(back_populates="expenses", lazy="selectin")

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id", ondelete="CASCADE"))
    department: Mapped["Department"] = relationship(back_populates="expenses", lazy="selectin")

    created_at = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
