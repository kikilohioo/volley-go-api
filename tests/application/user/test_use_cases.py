# tests/application/user/test_use_cases.py

from app.api.user.schemas import UserResponse

BASE_ROUTE = "/users"

# -------------------------
# TEST: OBTENER USUARIO POR ID
# -------------------------


def test_get_user_by_id(authorized_client, test_user):
    """
    Verifica que el usuario realmente se guarda en la base de datos de prueba.
    """

    res = authorized_client.get(f"{BASE_ROUTE}/{test_user.id}")

    user = UserResponse.model_validate(res.json())

    assert user is not None
    assert user.email == test_user.email
    assert user.full_name == test_user.full_name


# -------------------------
# TEST: OBTENER MI PROPIO USUARIO
# -------------------------
def test_get_my_user(authorized_client, test_user):
    """
    Verifica que el usuario realmente se guarda en la base de datos de prueba.
    """

    res = authorized_client.get(f"{BASE_ROUTE}/me")

    user = UserResponse.model_validate(res.json())

    assert user is not None
    assert user.email == test_user.email
    assert user.full_name == test_user.full_name
