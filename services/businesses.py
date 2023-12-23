from typing import List, Optional

import sqlalchemy.exc

from models import Business, Department, Expense

from schemas.businesses.business import BusinessesSchemaCreate, BusinessesSchemaUpdate
from schemas.businesses.department import DepartmentsSchemaCreate, DepartmentsSchemaUpdate
from schemas.businesses.expense import ExpenseSchemaCreate, ExpenseSchemaUpdate
from utils.unit_of_work import UnitOfWork


class BusinessesService:
    # Business
    @staticmethod
    async def create_business(uow: UnitOfWork, business_schema: BusinessesSchemaCreate) -> Business:
        async with uow:
            business = await uow.businesses.create(business_schema)
            await uow.commit()
            return business
    
    @staticmethod
    async def get_businesses(uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Business]:
        async with uow:
            businesses = await uow.businesses.get_all(offset=offset, limit=limit)
            return businesses
    
    @staticmethod
    async def get_business(uow: UnitOfWork, business_id: int) -> Business:
        async with uow:
            business = await uow.businesses.get(business_id)
            return business
    
    @staticmethod
    async def edit_business(uow: UnitOfWork, business_id: int, business_schema: BusinessesSchemaUpdate) -> Business:
        async with uow:
            business = await uow.businesses.edit(business_id, business_schema)
            await uow.commit()
            return business
    
    @staticmethod
    async def delete_business(uow: UnitOfWork, business_id: int):
        async with uow:
            await uow.businesses.delete(business_id)
            await uow.commit()
    
    # Department
    @staticmethod
    async def create_department(uow: UnitOfWork, department_schema: DepartmentsSchemaCreate) -> Department:
        async with uow:
            department = await uow.departments.create(department_schema)
            await uow.commit()
            return department
    
    @staticmethod
    async def get_departments(uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Department]:
        async with uow:
            departments = await uow.departments.get_all(offset=offset, limit=limit)
            return departments
    
    @staticmethod
    async def get_business_departments(uow: UnitOfWork, business_id: int, offset: int = 0, limit: Optional[int] = None) -> List[Expense]:
        async with uow:
            departments = await uow.departments.filter(offset=offset, limit=limit, business_id=business_id)
            return departments
    
    @staticmethod
    async def get_department(uow: UnitOfWork, department_id: int) -> Department:
        async with uow:
            department = await uow.departments.get(department_id)
            return department
    
    @staticmethod
    async def edit_department(uow: UnitOfWork, department_id: int, department_schema: DepartmentsSchemaUpdate) -> Department:
        async with uow:
            department = await uow.departments.edit(department_id, department_schema)
            await uow.commit()
            return department
    
    @staticmethod
    async def delete_department(uow: UnitOfWork, department_id: int):
        async with uow:
            await uow.departments.delete(department_id)
            await uow.commit()
    
    # Expense
    @staticmethod
    async def create_expense(uow: UnitOfWork, expense_schema: ExpenseSchemaCreate) -> Expense:
        async with uow:
            try:
                department: Department = await uow.departments.get(expense_schema.department_id)

                if not department:
                    raise sqlalchemy.exc.NoResultFound("Department not found")

                # Проверяем, не превышает ли новый расход бюджет отдела
                if (department.budget - expense_schema.amount) < 0:
                    raise ValueError("Expense exceeds department budget")

                expense: Expense = await uow.expenses.create(expense_schema)

                # Обновляем текущий бюджет отдела
                department.budget -= expense.amount

                await uow.commit()
                return expense
            except sqlalchemy.exc.IntegrityError:  # на всякий случай
                await uow.rollback()
                raise ValueError("Integrity error: Unable to create expense")

    @staticmethod
    async def get_expenses(uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Expense]:
        async with uow:
            expenses = await uow.expenses.get_all(offset=offset, limit=limit)
            return expenses
    
    @staticmethod
    async def get_department_expenses(uow: UnitOfWork, department_id: int, offset: int = 0, limit: Optional[int] = None) -> List[Expense]:
        async with uow:
            expenses = await uow.expenses.filter(offset=offset, limit=limit, department_id=department_id)
            return expenses
    
    @staticmethod
    async def get_expense(uow: UnitOfWork, expense_id: int) -> Expense:
        async with uow:
            expense = await uow.expenses.get(expense_id)
            return expense
    
    @staticmethod
    async def edit_expense(uow: UnitOfWork, expense_id: int, expense_schema: ExpenseSchemaUpdate) -> Expense:
        async with uow:
            try:
                expense: Expense = await uow.expenses.get(expense_id)

                if not expense:
                    raise sqlalchemy.exc.NoResultFound("Expense not found")

                # Проверяем, не превышает ли изменённый расход бюджет отдела (не включая изначальную сумму расхода)
                diff_between_current_and_new_value = expense_schema.amount - expense.amount
                if expense.department.budget - diff_between_current_and_new_value < 0:
                    raise ValueError("Expense exceeds department budget")

                # expense: Expense = await uow.expenses.create(expense_schema)
                expense = await uow.expenses.edit(expense_id, expense_schema)

                # Обновляем текущий бюджет отдела
                expense.department.budget -= diff_between_current_and_new_value

                await uow.commit()
                return expense
            except sqlalchemy.exc.IntegrityError:  # на всякий случай
                raise ValueError("Integrity error: Unable to create expense")
    
    @staticmethod
    async def delete_expense(uow: UnitOfWork, expense_id: int):
        async with uow:
            expense: Expense = await uow.expenses.get(expense_id)

            if expense:
                expense.department.budget += expense.amount

                await uow.expenses.delete(expense_id)
                await uow.commit()
