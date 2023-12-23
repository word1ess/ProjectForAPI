from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.utils.sockets import notify_clients
from api.utils.dependencies import UOWDep
from schemas.businesses.expense import ExpenseSchema, ExpenseSchemaCreate, ExpenseSchemaUpdate
from services.businesses import BusinessesService

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.post("/", response_model=ExpenseSchema)
async def create_expense(uow: UOWDep, expense_schema: ExpenseSchemaCreate):
    try:
        expense = await BusinessesService().create_expense(uow, expense_schema)

        await notify_clients(f"Created the expense '(ID: {expense.id})' "
                             f"for the department '{expense.department.title} (ID: {expense.department_id})'")
        return expense
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e)


@router.get("/", response_model=List[ExpenseSchema])
async def read_expenses(uow: UOWDep, offset: int = 0, limit: int = 10):
    expenses = await BusinessesService().get_expenses(uow, offset=offset, limit=limit)
    return expenses


@router.get("/{expense_id}", response_model=ExpenseSchema)
async def read_expense(uow: UOWDep, expense_id: int):
    expense = await BusinessesService().get_expense(uow, expense_id)
    return expense


@router.patch("/{expense_id}", response_model=ExpenseSchema)
async def update_expense(uow: UOWDep, expense_id: int, expense_schema: ExpenseSchemaUpdate):
    try:
        expense = await BusinessesService().edit_expense(uow, expense_id, expense_schema)
        await notify_clients(f"Updated expense '(ID: {expense.id})' "
                             f"of the department '{expense.department.title} (ID: {expense.department_id})'")
        return expense
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expense not found")


@router.delete("/{expense_id}")
async def delete_expense(uow: UOWDep, expense_id: int):
    try:
        await BusinessesService().delete_expense(uow, expense_id)

        await notify_clients(f"Deleted expense '(ID :{expense_id})'")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"expense": "Expense deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expense not found")
