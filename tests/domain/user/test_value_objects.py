import pytest
from app.domain.user.value_objects import Email, Password, UserRole


# -------------------------
# TEST: VALID EMAIL
# -------------------------
def test_email_valid():
    email = Email("test@example.com")
    assert email.value == "test@example.com"


# -------------------------
# TEST: INVALID EMAIL
# -------------------------
def test_email_invalid():
    with pytest.raises(ValueError):
        Email("invalid-email")


# -------------------------
# TEST: VALID PASSWORD
# -------------------------
def test_password_valid():
    pw = Password("12345678")
    assert pw.value == "12345678"


# -------------------------
# TEST: INVALID PASSWORD TOO SHORT
# -------------------------
def test_password_too_short():
    with pytest.raises(ValueError):
        Password("1234567")  # menos de 8 chars


# -------------------------
# TEST: VALID ROLE
# -------------------------
def test_role_valid():
    role = UserRole("player")
    assert role.value == "player"


# -------------------------
# TEST: INVALID ROLE
# -------------------------
def test_role_invalid():
    with pytest.raises(ValueError):
        UserRole("invalid")
