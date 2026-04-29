from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.api.main import api_router
from app.core.config import settings
from app.core.exceptions import AppError

app = FastAPI(title=settings.PROJECT_NAME)


@app.exception_handler(AppError)
async def service_exception_handler(request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"type": exc.code, "message": exc.message}},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"type": "http_error", "message": exc.detail}},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_server_error",
                "message": "An unexpected error occurred.",
            }
        },
    )


# include api routers
app.include_router(api_router, prefix=settings.API_STR)
