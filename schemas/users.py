from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserSchemaBase(BaseModel):
    name: str


class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchemaUpdate(UserSchemaBase):
    name: Optional[str] = None


class UserSchema(UserSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime
    updated_at: datetime
