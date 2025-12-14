# app/api/auth/exception_handlers.py

import inspect
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.domain.championship import exceptions as championship_exceptions
from app.domain.championship.exceptions import ChampionshipDomainException

def generate_exception_map():
    mapping = {}

    # Obtenemos todas las clases dentro del módulo
    for name, obj in inspect.getmembers(championship_exceptions, inspect.isclass):

        # Filtramos solo clases que hereden de ChampionshipDomainException
        if issubclass(obj, championship_exceptions.ChampionshipDomainException) \
                and obj is not championship_exceptions.ChampionshipDomainException:

            # Podés definir reglas automáticas
            if "NotFound" in name:
                mapping[obj] = (status.HTTP_404_NOT_FOUND, name.replace("Exception", ""))
            else:
                mapping[obj] = (status.HTTP_400_BAD_REQUEST, name.replace("Exception", ""))

    return mapping


exception_map = generate_exception_map()


async def championship_exception_handler(request: Request, exc: ChampionshipDomainException):
    status_code, default_message = exception_map.get(
        type(exc), (500, "User domain error"))
    
    message = str(exc) if str(exc).strip() else default_message

    return JSONResponse(status_code=status_code, content={"detail": message})
