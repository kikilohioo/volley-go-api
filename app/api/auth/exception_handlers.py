# app/api/auth/exception_handlers.py

import inspect
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.domain.user import exceptions as user_exceptions
from app.domain.user.exceptions import UserDomainException


def generate_exception_map():
    mapping = {}

    # Obtenemos todas las clases dentro del módulo
    for name, obj in inspect.getmembers(user_exceptions, inspect.isclass):

        # Filtramos solo clases que hereden de UserDomainException
        if issubclass(obj, UserDomainException) \
                and obj is not UserDomainException:

            # Podés definir reglas automáticas
            if "NotFound" in name:
                mapping[obj] = (status.HTTP_404_NOT_FOUND,
                                name.replace("Exception", ""))
            else:
                mapping[obj] = (status.HTTP_400_BAD_REQUEST,
                                name.replace("Exception", ""))

    return mapping


exception_map = generate_exception_map()


async def auth_exception_handler(request: Request, exc: UserDomainException):
    status_code, default_message = exception_map.get(
        type(exc), (500, "User domain error"))
    
    message = str(exc) if str(exc).strip() else default_message

    return JSONResponse(status_code=status_code, content={"detail": message})
