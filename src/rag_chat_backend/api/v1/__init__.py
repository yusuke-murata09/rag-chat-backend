from fastapi import APIRouter

from .health_chek import router as healthcheck_router

router = APIRouter()
router.include_router(healthcheck_router, prefix="/healthcheck", tags=["healthcheck"])
