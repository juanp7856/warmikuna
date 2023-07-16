import pytest
from funciones.val_reset import valreset

@pytest.mark.parametrize(
    "user_id,new_password,confirm_password,resultado",
    [
        ("1", "juan12345", "juan12345", ""), #ESCENARIO ACERTADO
        (None, "juan12345", "juan12345", ""), #ESCENARIO ERRÓNEO
        ("1", "jj", "123", ""), #ESCENARIO ERRÓNEO
        (None, "juan12345", "juan12345", "No se encontró id de usuario.") #ESCENARIO ACERTADO
    ]
)
def test_val_reset(user_id, new_password, confirm_password, resultado):
    assert valreset(user_id, new_password, confirm_password) == resultado

