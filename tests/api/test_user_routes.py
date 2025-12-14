# tests/api/test_user_routes.py

from app.api.user.schemas import UserResponse


BASE_ROUTE = '/users'


# -------------------------
# TEST: OBTENER UN USUARIO POR ID
# -------------------------
def test_get_user_by_id_api(test_user, authorized_client):
    '''
    Verifica que se pueda crear un usuario correctamente
    y que los datos devueltos coincidan con los esperados.
    '''

    res = authorized_client.get(f'{BASE_ROUTE}/{test_user.id}/')

    user = UserResponse.model_validate(res.json())

    assert res.status_code == 200
    assert user.id == test_user.id
    assert user.email == test_user.email
    assert user.status == test_user.status
