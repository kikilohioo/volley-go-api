# tests/application/auth/test_use_cases.py

from app.api.user.schemas import UserResponse

BASE_ROUTE = "/auth"
REGISTER_ROUTE = f"{BASE_ROUTE}/register/"


# -------------------------
# TEST: CREAR USUARIO
# -------------------------
def test_register_user_success(client, create_user_payload_json):
    """
    Debe crear el usuario correctamente vía API /users/
    """
    res = client.post(REGISTER_ROUTE, json=create_user_payload_json)

    assert res.status_code == 201, res.text

    data = res.json()
    user = UserResponse.model_validate(data)

    # No debe venir contraseña
    assert "password" not in data
    assert user.email == create_user_payload_json["email"]
    assert user.full_name == create_user_payload_json["full_name"]


# -------------------------
# TEST: EMAIL DUPLICADO
# -------------------------
def test_register_user_email_duplicate(client, create_user_payload_json):
    """
    No debe permitir crear dos usuarios con el mismo email.
    """
    # primer usuario OK
    res1 = client.post(REGISTER_ROUTE, json=create_user_payload_json)
    assert res1.status_code == 201

    # segundo usuario con el MISMO EMAIL
    res2 = client.post(REGISTER_ROUTE, json=create_user_payload_json)

    assert res2.status_code == 409
    assert res2.json().get("detail") == "User with that email already exists"


# -------------------------
# TEST: PERSISTENCIA REAL EN BD
# -------------------------
def test_user_persisted_in_database(client, db_session, create_user_payload_json):
    """
    Verifica que el usuario realmente se guarda en la base de datos de prueba.
    """

    client.post(REGISTER_ROUTE, json=create_user_payload_json)

    # consulta directa a SQLAlchemy
    from app.infrastructure.user.sqlalchemy_user_model import UserModel

    user_in_db = (
        db_session.query(UserModel)
        .filter(UserModel.email == create_user_payload_json["email"])
        .first()
    )

    assert user_in_db is not None
    assert user_in_db.email == create_user_payload_json["email"]
    assert user_in_db.full_name == create_user_payload_json["full_name"]
    assert user_in_db.password != ""  # password debe estar hasheado
