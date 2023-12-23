from decimal import Decimal
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ExpenseSchemaBase(BaseModel):
    amount: Decimal = Field(..., ge=0, lt=10000000000)
    description: str
    expense_date: date
    department_id: int
    creator_id: int


class ExpenseSchemaCreate(ExpenseSchemaBase):
    pass


class ExpenseSchemaUpdate(ExpenseSchemaBase):
    amount: Optional[Decimal] = Field(None, ge=0, lt=10000000000)
    description: Optional[str] = None
    expense_date: Optional[date] = None
    department_id: Optional[int] = None
    creator_id: Optional[int] = None


class ExpenseSchema(ExpenseSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
