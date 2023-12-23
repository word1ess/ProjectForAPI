from datetime import datetime
from typing import Optional

from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class DepartmentsSchemaBase(BaseModel):
    title: str
    allocated_budget: Decimal = Field(..., ge=0, lt=10000000000)
    budget: Decimal = Field(..., ge=0, lt=10000000000)
    director_id: int
    business_id: int


class DepartmentsSchemaCreate(DepartmentsSchemaBase):
    pass


class DepartmentsSchemaUpdate(DepartmentsSchemaBase):
    title: Optional[str] = None
    allocated_budget: Optional[Decimal] = Field(None, ge=0, lt=10000000000)
    budget: Optional[Decimal] = Field(None, ge=0, lt=10000000000)
    director_id: Optional[int] = None
    business_id: Optional[int] = None


class DepartmentsSchema(DepartmentsSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
