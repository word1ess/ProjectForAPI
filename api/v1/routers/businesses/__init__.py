from fastapi import APIRouter

from .business import router as business_router
from .department import router as department_router
from .expense import router as product_router

# Определение основного роутера
router = APIRouter()

router.include_router(business_router)
router.include_router(department_router, prefix="/businesses")
router.include_router(product_router, prefix="/businesses/departments")
