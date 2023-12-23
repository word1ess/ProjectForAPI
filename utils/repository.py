from pydantic import BaseModel as BaseSchema
from db import Base as ModelBase
from typing import Sequence

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj_data: BaseSchema | dict) -> ModelBase:
        obj_data = obj_data if isinstance(obj_data, dict) else obj_data.model_dump()

        stmt = insert(self.model).values(**obj_data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(
            self, offset: int = 0, limit: int | None = None
    ) -> Sequence[ModelBase]:
        stmt = select(self.model).offset(offset=offset)

        if limit:
            stmt = stmt.limit(limit=limit)

        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items

    async def get(self, obj_id: int) -> ModelBase:
        stmt = select(self.model).filter_by(id=obj_id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit(self, obj_id: int, obj_data: BaseSchema | dict) -> int:
        obj_data = obj_data if isinstance(obj_data, dict) else obj_data.model_dump()

        stmt = (
            update(self.model)
            .values(**obj_data)
            .filter_by(id=obj_id)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, obj_id: int):
        stmt = delete(self.model).filter_by(id=obj_id)
        await self.session.execute(stmt)

    async def filter(
            self,
            offset: int = 0,
            limit: int | None = None,
            **filter_by
    ):
        stmt = select(self.model).offset(offset=offset)

        if limit:
            stmt = stmt.limit(limit=limit)

        if filter_by:
            valid_attributes = {
                attr: value
                for attr, value in filter_by.items()
                if hasattr(self.model, attr)
            }

            stmt = stmt.filter_by(**valid_attributes)

        result = await self.session.execute(stmt)

        return result.scalars().all()
