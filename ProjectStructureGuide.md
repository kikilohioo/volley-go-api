# Esto es una guia rapida y simplificada de como se extiende el proyecto con DDD
Es un poco enrredado al inicio, pero reporta muy buenos beneficios, como el desacople de tecnologias, el aislamiento de la logica de negocios, mejoras en la testeabilidad y escalabilidad del proyecto en terminos del codigo y del equipo.

## ESTRUCTURA DEL PROYECTO
```
/alembic
├─ versions/            # Solo se tocan los archivos aquí luego de crear una migración
# ...

app/
├─ api/                 # Routers o controllers con sus dependencias, schemas, etc
│  ├─ auth/             # Lo mismo que user (register, login, etc)
│  └─ user/
│     ├─ dependencies.py        # Para inyección de dependencias
│     ├─ exceptions_handlers.py # Manejo de excepciones (ej: email duplicado)
│     ├─ routes.py              # Definición de rutas / path operations
│     ├─ schemas.py             # Validación de requests/responses
│     └─ schemas_internal.py    # Schemas para uso interno (ej: testing)
# Aquí se podrían crear más carpetas de entidades (ej: posts)
# ...

├─ application/        # Lógica de aplicación y casos de uso
│  ├─ auth/            # Lo mismo que user pero para autenticación
│  ├─ user/
│  |  └─ use_cases.py  # Casos de uso: get user by id, get my user, etc
|  ├─ mappers.py              # Funcion generica de mapeo entre schemas y dominio
# Aquí se podrían crear más carpetas de entidades (ej: posts)
# ...

├─ core/               # Configuraciones y utilidades
│  └─ config.py        # Carga de variables de entorno desde .env o container

├─ domain/             # Reglas de negocio (no incluye auth porque no es logica del negocio)
│  └─ user/
│     ├─ entities.py       # Modelo de negocio (User)
│     ├─ exceptions.py     # Excepciones de negocio (ej: email duplicado)
│     ├─ repositories.py   # Interface de repositorios (IUserRepository)
│     └─ value_objects.py  # Validaciones de entity (Email, Password, Role)
# Aquí se podrían crear más carpetas de entidades (ej: posts)
# ...

├─ infrastructure/     # Implementaciones concretas
│  ├─ auth/
│  │  ├─ dependencies.py   # Dependencias para OAuth2
│  │  ├─ jwt_service.py    # Gestión de JWT
│  │  └─ password_service.py # Gestión de contraseñas
│  ├─ user/
│  │  ├─ sqlalchemy_repository.py # Implementación de IUserRepository
│  │  └─ sqlalchemy_user_model.py # Modelo ORM de User
│  ├─ mappers.py              # Funcion generica de mapeo entre ORM y dominio
│  └─ database.py
│
└─ main.py             # Entry point de la app

/tests
├─ api/                # Tests para rutas
│  ├─ test_auth_routers.py
│  └─ test_user_routers.py
# Aquí se podrían crear más tests de rutas (ej: posts)
# ...

├─ application/        # Tests de casos de uso
│  ├─ auth/
│  └─ user/
│     └─ test_user_use_cases.py
# Aquí se podrían crear más tests de application (ej: posts)
# ...

├─ domain/             # Tests de negocio
│  └─ user/
│     ├─ test_user_entity.py       # Tests de la entidad
│     └─ test_value_objects.py    # Tests de las validaciones (VO)
# Aquí se podrían crear más tests de dominio (ej: posts)
# ...

├─ infrastructure/     # Tests de implementaciones concretas
│  └─ test_user_repository.py
# Aquí se podrían crear más tests de infrastructure (ej: posts)
# ...

└─ conftest.py         # Fixtures compartidos para tests
```

## Classes a mantener de forma independiente por entidad
- Entity models (app/domain/<entity>)
- Request/Response schemas (app/api/<entity>)
- ORM models (app/infrastructure/<entity>)

## Paso a Paso recomendado para agregar nuevas entidades(ej: championship)
1. Dominio (domain/championship)
    - Entities: define la entidad Championship y sus atributos principales.
    - Value objects: si tienes atributos que necesitan validación (por ejemplo Name, DateRange, etc.), crea value objects.
    - Exceptions: excepciones de negocio (por ejemplo ChampionshipAlreadyExists, InvalidChampionshipDate).
    - Repositories interface: define IChampionshipRepository con métodos como create, get_by_id, update, delete.

2. Infraestructura (infrastructure/championship)
    - ORM models: crea el modelo SQLAlchemy ChampionshipModel.
    - Repositories: implementa IChampionshipRepository usando SQLAlchemy.
    - Mappers: funciones que convierten entre entidad de dominio y modelo ORM.

3. Application (application/championship/use_cases.py)
    - Crea los casos de uso:
        - CreateChampionshipUseCase
        - GetChampionshipByIdUseCase
        - UpdateChampionshipUseCase
    - Cada use case recibe el repositorio como dependencia y aplica la lógica de aplicación.

4. API (api/championship)
    - Schemas: request y response schemas usando Pydantic (ChampionshipCreateRequest, ChampionshipResponse).
    - Routes: define rutas REST (/championships) usando los use cases.
    - Dependencies: si necesitas inyección del repositorio.
    - Exception handlers: registra las excepciones específicas de esta entidad.

5. Alembic
    - Genera migraciones para la nueva tabla championships.

6. Tests
    - Domain: test_value_objects.py y test_entities.py.
    - Application: tests para cada use case (crear, actualizar, obtener).
    - Infrastructure: tests de repositorio con DB temporal.
    - API: tests de rutas usando TestClient o AsyncClient.
