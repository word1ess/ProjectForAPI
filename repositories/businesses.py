from models import Business, Department, Expense
from utils.repository import SQLAlchemyRepository


class BusinessesRepository(SQLAlchemyRepository):
    model = Business


class DepartmentsRepository(SQLAlchemyRepository):
    model = Department


class ExpensesRepository(SQLAlchemyRepository):
    model = Expense
