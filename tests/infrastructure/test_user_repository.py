# tests/infrastructure/test_user_repository.py

from app.domain.user.entities import User
from app.infrastructure.user.sqlalchemy_repository import SQLAlchemyUserRepository


# -------------------------
# TEST: GET BY EMAIL
# -------------------------
def test_get_by_email(db_session):
    repo = SQLAlchemyUserRepository(db_session)

    # insertar manualmente
    user = User(
        id=None,
        email="example@mail.com",
        password="hashed",
        full_name="User",
        role="player",
        avatar_url="avatar_url",
        status=True
    )

    created = repo.create(user)
    fetched = repo.get_by_email("example@mail.com")

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.email == "example@mail.com"


# -------------------------
# TEST: GET BY ID
# -------------------------
def test_get_by_id(db_session):
    repo = SQLAlchemyUserRepository(db_session)

    # insertar manualmente
    user = User(
        id=None,
        email="new_example@mail.com",
        password="hashed",
        full_name="User",
        role="player",
        avatar_url="avatar_url",
        status=True
    )

    created = repo.create(user)
    fetched = repo.get_by_id(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.email == "new_example@mail.com"


# -------------------------
# TEST: CREATE USER
# -------------------------
def test_create_user(db_session):
    repo = SQLAlchemyUserRepository(db_session)

    user = User(
        id=None,
        email="test_create@mail.com",
        password="hashed_pw",
        full_name="Test Create",
        role="player",
        avatar_url="avatar_url",
        status=True
    )

    created = repo.create(user)

    # Verificaciones
    assert created.id is not None
    assert created.email == "test_create@mail.com"
    assert created.full_name == "Test Create"

    # Confirmar que quedó en la base
    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.email == "test_create@mail.com"


# -------------------------
# TEST: UPDATE USER
# -------------------------
def test_update_user(db_session):
    repo = SQLAlchemyUserRepository(db_session)

    # Crear usuario inicial
    user = User(
        id=None,
        email="update_test@mail.com",
        password="pw_old",
        full_name="Old Name",
        role="player",
        avatar_url="old_avatar",
        status=True
    )

    created = repo.create(user)

    # Modificar el usuario
    created.full_name = "New Name"
    created.avatar_url = "new_avatar"

    updated = repo.update(created)

    # Verificaciones
    assert updated.full_name == "New Name"
    assert updated.avatar_url == "new_avatar"

    # Confirmar en DB
    fetched = repo.get_by_id(updated.id)
    assert fetched.full_name == "New Name"
    assert fetched.avatar_url == "new_avatar"
