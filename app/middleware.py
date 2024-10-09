from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .logger import logger

class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            logger.error(f"(Mid)HTTPException: {exc.detail}")
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        except Exception as exc:
            logger.error(f"(Mid)Unhandled Exception: {str(exc)}", exc_info=True)
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
