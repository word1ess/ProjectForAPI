from fastapi import APIRouter, HTTPException

from api.utils.dependencies import UOWDep
from schemas.users import UserSchemaCreate, UserSchema, UserSchemaUpdate
from services.users import UsersService

from typing import List

from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import status
from fastapi.responses import JSONResponse

from api.utils.sockets import notify_clients

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/login", response_model=UserSchema)
async def login(uow: UOWDep, user_schema: UserSchemaCreate):
    try:
        user = await UsersService().get_user_by_name(uow, user_name=user_schema.model_dump().get('name'))
        await notify_clients(f"User {user.name} logged in!")
        return user
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")


@router.post("/", response_model=UserSchema)
async def create_user(uow: UOWDep, user_schema: UserSchemaCreate):
    try:
        user = await UsersService().create_user(uow, user_schema)
        await notify_clients(f"User created: {user.name}")
        return user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists")


@router.get("/", response_model=List[UserSchema])
async def read_users(uow: UOWDep, offset: int = 0, limit: int = 10):
    users = await UsersService().get_users(uow, offset=offset, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(uow: UOWDep, user_id: int):
    user = await UsersService().get_user(uow, user_id)
    return user


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(uow: UOWDep, user_id: int, user_schema: UserSchemaUpdate):
    try:
        user = await UsersService().edit_user(uow, user_id, user_schema)
        await notify_clients(f"User updated: {user.name}")
        return user
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")


@router.delete("/{user_id}")
async def delete_user(uow: UOWDep, user_id: int):
    try:
        await UsersService().delete_user(uow, user_id)

        await notify_clients(f"User deleted: ({user_id} ID)")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"product": "User deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
