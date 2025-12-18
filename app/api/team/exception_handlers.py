# app/api/auth/exception_handlers.py

import inspect
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.domain.team import exceptions as team_exceptions
from app.domain.team.exceptions import TeamDomainException

def generate_exception_map():
    mapping = {}

    # Obtenemos todas las clases dentro del módulo
    for name, obj in inspect.getmembers(team_exceptions, inspect.isclass):

        # Filtramos solo clases que hereden de TeamDomainException
        if issubclass(obj, team_exceptions.TeamDomainException) \
                and obj is not team_exceptions.TeamDomainException:

            # Podés definir reglas automáticas
            if "NotFound" in name:
                mapping[obj] = (status.HTTP_404_NOT_FOUND, name.replace("Exception", ""))
            else:
                mapping[obj] = (status.HTTP_400_BAD_REQUEST, name.replace("Exception", ""))

    return mapping


exception_map = generate_exception_map()


async def team_exception_handler(request: Request, exc: TeamDomainException):
    status_code, default_message = exception_map.get(
        type(exc), (500, "User domain error"))
    
    message = str(exc) if str(exc).strip() else default_message

    return JSONResponse(status_code=status_code, content={"detail": message})
