# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import routers
from app.api.routes import router as main_router
from app.api.user.routes import router as user_router
from app.api.auth.routes import router as auth_router
from app.api.championship.routes import router as championship_router

# Import exception handlers and exceptions
from app.domain.user.exceptions import UserDomainException
from app.api.user.exception_handlers import user_exception_handler

from app.domain.user.exceptions import UserDomainException
from app.api.auth.exception_handlers import auth_exception_handler

from app.domain.championship.exceptions import ChampionshipDomainException
from app.api.championship.exception_handlers import championship_exception_handler


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Register exception handlers
app.add_exception_handler(UserDomainException, user_exception_handler)
app.add_exception_handler(UserDomainException, auth_exception_handler)
app.add_exception_handler(ChampionshipDomainException,
                          championship_exception_handler)

# Include routers
app.include_router(main_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(championship_router)

app.mount(
    "/media/avatars",
    StaticFiles(directory="app/infrastructure/storage/avatars"),
    name="avatars"
)

app.mount(
    "/media/championships",
    StaticFiles(directory="app/infrastructure/storage/championships"),
    name="championships"
)
