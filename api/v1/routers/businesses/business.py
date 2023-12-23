from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.utils.sockets import notify_clients
from api.utils.dependencies import UOWDep
from schemas.businesses.business import BusinessesSchema, BusinessesSchemaCreate, BusinessesSchemaUpdate
from schemas.businesses.department import DepartmentsSchema
from services.businesses import BusinessesService

router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"],
)


@router.post("/", response_model=BusinessesSchema)
async def create_business(uow: UOWDep, business_schema: BusinessesSchemaCreate):
    business = await BusinessesService().create_business(uow, business_schema)
    await notify_clients(f"Created the business '{business.title}' "
                         f"for the owner '{business.owner.name} (ID: {business.owner_id})'")
    return business


@router.get("/", response_model=List[BusinessesSchema])
async def read_businesses(uow: UOWDep, offset: int = 0, limit: int = 10):
    businesses = await BusinessesService().get_businesses(uow, offset=offset, limit=limit)
    return businesses


@router.get("/{business_id}", response_model=BusinessesSchema)
async def read_business(uow: UOWDep, business_id: int):
    business = await BusinessesService().get_business(uow, business_id)
    return business


@router.get("/{business_id}/departments/", response_model=List[DepartmentsSchema])
async def read_business_departments(uow: UOWDep, business_id: int, offset: int = 0, limit: int = 10):
    try:
        products = await BusinessesService().get_business_departments(uow, business_id=business_id, offset=offset, limit=limit)
        return products
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Departments not found")


@router.patch("/{business_id}", response_model=BusinessesSchema)
async def update_business(uow: UOWDep, business_id: int, business_schema: BusinessesSchemaUpdate):
    try:
        business = await BusinessesService().edit_business(uow, business_id, business_schema)
        await notify_clients(f"Updated the business '{business.title} (ID: {business.id})' "
                             f"owner '{business.owner.name} (ID: {business.owner_id})'")
        return business
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Business not found")


@router.delete("/{business_id}")
async def delete_business(uow: UOWDep, business_id: int):
    try:
        await BusinessesService().delete_business(uow, business_id)

        await notify_clients(f"Deleted the business (ID: '{business_id})'")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"product": "Business deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Business not found")
