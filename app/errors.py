import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("app")

async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database operation failed"},
    )


async def external_api_handler(request: Request, exc: RequestException):
    logger.exception(f"External API error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": "Failed to contact external service"},
    )