from datetime import datetime
from app.domain.user.entities import User
from app.domain.user.value_objects import Email, Password, UserRole


# -------------------------
# TEST: USER ENTITY BASIC CREATION
# -------------------------
def test_create_user_entity_basic():
    user = User(
        id=None,
        email=Email("test@example.com"),
        password=Password("12345678"),
        full_name="Test User",
        role=UserRole("player"),
        avatar_url=None
    )

    assert user.full_name == "Test User"
    assert user.email.value == "test@example.com"
    assert user.password.value == "12345678"
    assert user.role.value == "player"
    assert user.status is True
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


# -------------------------
# TEST: USER ENTITY WITH DEFAULT VALUES
# -------------------------
def test_user_entity_has_default_values():
    user = User(
        id=1,
        email=Email("admin@example.com"),
        password=Password("strongpass"),
        full_name="Admin",
        role=UserRole("organizer"),
        avatar_url="avatar.png"
    )

    assert user.status is True
    assert user.avatar_url == "avatar.png"
    assert user.id == 1
