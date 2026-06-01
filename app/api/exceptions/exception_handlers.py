from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Error {exc.status_code}: {exc.detail}"},
    )


def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = []
    for error in exc.errors():
        err = error.copy()
        if "ctx" in err and "error" in err["ctx"]:
            err["ctx"]["error"] = str(err["ctx"]["error"])
        errors.append(err)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"message": "Invalid input", "errors": errors},
    )
