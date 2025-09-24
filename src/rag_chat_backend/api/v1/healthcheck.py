from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("")
def healthcheck() -> JSONResponse:
    return JSONResponse(content={"success": True})
