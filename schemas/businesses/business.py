from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BusinessesSchemaBase(BaseModel):
    title: str
    owner_id: int


class BusinessesSchemaCreate(BusinessesSchemaBase):
    pass


class BusinessesSchemaUpdate(BusinessesSchemaBase):
    title: Optional[str] = None
    owner_id: Optional[int] = None


class BusinessesSchema(BusinessesSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
