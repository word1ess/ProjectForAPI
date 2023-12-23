from typing import List

from sqlalchemy.exc import NoResultFound

from models import User
from schemas.users import UserSchemaCreate, UserSchemaUpdate
from utils.unit_of_work import UnitOfWork


class UsersService:
    @staticmethod
    async def create_user(uow: UnitOfWork, user_schema: UserSchemaCreate) -> User:
        async with uow:
            user = await uow.users.create(user_schema)
            await uow.commit()
            return user

    @staticmethod
    async def get_user(uow: UnitOfWork, user_id: int) -> User:
        async with uow:
            user = await uow.users.get(user_id)
            return user

    @staticmethod
    async def get_user_by_name(uow: UnitOfWork, user_name: str) -> User:
        async with uow:
            user = await uow.users.filter(name=user_name)
            if not user:
                raise NoResultFound
            return user[0]

    @staticmethod
    async def get_users(uow: UnitOfWork, offset: int = 0, limit: int | None = None) -> List[User]:
        async with uow:
            users = await uow.users.get_all(offset=offset, limit=limit)
            return users

    @staticmethod
    async def edit_user(uow: UnitOfWork, user_id: int, user_schema: UserSchemaUpdate) -> User:
        async with uow:
            user = await uow.users.edit(user_id, user_schema)
            await uow.commit()
            return user

    @staticmethod
    async def delete_user(uow: UnitOfWork, user_id: int):
        async with uow:
            await uow.users.delete(user_id)
            await uow.commit()
