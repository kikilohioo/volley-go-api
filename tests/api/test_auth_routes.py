# tests/api/test_auth_routes.py

BASE_ROUTE = "/auth"
REGISTER_ROUTE = f"{BASE_ROUTE}/register/"

# -------------------------
# TEST: CREAR USUARIO
# -------------------------
def test_register_user_api(test_user, create_user_payload):
    '''
    Verifica que se pueda crear un usuario correctamente
    y que los datos devueltos coincidan con los esperados.
    '''
    assert test_user.email == create_user_payload.email
    assert test_user.full_name == create_user_payload.full_name
    assert test_user.role == 'player'
    assert test_user.id, 'Debe devolverse un ID'
    assert test_user.created_at, 'Debe incluir una fecha de creación'


# -------------------------
# TEST: CREAR USUARIO QUE YA EXISTE
# -------------------------
def test_register_allready_registered_user_api(test_user, client, create_user_payload_json):
    '''
    Verifica que se pueda crear un usuario correctamente
    y que los datos devueltos coincidan con los esperados.
    '''
    res = client.post(REGISTER_ROUTE, json=create_user_payload_json)

    assert res.status_code == 409, res.text
