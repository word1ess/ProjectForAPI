from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.utils.sockets import notify_clients
from api.utils.dependencies import UOWDep
from schemas.businesses.department import DepartmentsSchema, DepartmentsSchemaCreate, DepartmentsSchemaUpdate
from schemas.businesses.expense import ExpenseSchema
from services.businesses import BusinessesService

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.post("/", response_model=DepartmentsSchema)
async def create_department(uow: UOWDep, department_schema: DepartmentsSchemaCreate):
    department = await BusinessesService().create_department(uow, department_schema)
    await notify_clients(f"Created the department '{department.title} (ID: {department.id})' "
                         f"for the business '{department.business.title} (ID: {department.business_id})' "
                         f"with budget '{department.allocated_budget}'₽")
    return department


@router.get("/", response_model=List[DepartmentsSchema])
async def read_departments(uow: UOWDep, offset: int = 0, limit: int = 10):
    departments = await BusinessesService().get_departments(uow, offset=offset, limit=limit)
    return departments


@router.get("/{department_id}", response_model=DepartmentsSchema)
async def read_department(uow: UOWDep, department_id: int):
    try:
        department = await BusinessesService().get_department(uow, department_id)
        return department
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Department not found")


@router.get("/{department_id}/expenses/", response_model=List[ExpenseSchema])
async def read_department_expenses(uow: UOWDep, department_id: int, offset: int = 0, limit: int = 10):
    try:
        expenses = await BusinessesService().get_department_expenses(uow, department_id=department_id, offset=offset,
                                                                     limit=limit)
        return expenses
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expenses not found")


@router.patch("/{department_id}", response_model=DepartmentsSchema)
async def update_department(uow: UOWDep, department_id: int, department_schema: DepartmentsSchemaUpdate):
    try:
        department = await BusinessesService().edit_department(uow, department_id, department_schema)
        await notify_clients(f"Updated the department '{department.title} (ID: {department.id})' was created "
                             f"of business '{department.business.title} (ID: {department.business_id})'")
        return department
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Department not found")


@router.delete("/{department_id}")
async def delete_department(uow: UOWDep, department_id: int):
    try:
        await BusinessesService().delete_department(uow, department_id)

        await notify_clients(f"Deleted the department '(ID: {department_id})'")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"product": "Department deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Department not found")
