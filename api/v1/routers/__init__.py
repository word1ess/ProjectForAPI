from fastapi import APIRouter

from api.v1.routers.users import router as users_router
from api.v1.routers.businesses import router as businesses_router

router = APIRouter(prefix='/v1')

router.include_router(users_router)
router.include_router(businesses_router)
