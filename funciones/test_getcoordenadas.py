import pytest

from get_coordenadas import get_coordenadas

@pytest.mark.parametrize(
    "departamento,resultado",
    [
        ("Lima", [-12.046374, -77.042793]), #ESCENARIO ACERTADO
        ("Arequipa", [-12.046374, -77.042793]), #ESCENARIO ERRÓNEO
        ("Washington", [0, 0]), #ESCENARIO ACERTADO
        ("Washington", [1, 2]) #ESCENARIO ERRÓNEO
    ]
)
def test_get_coordenadas(departamento, resultado):
    assert get_coordenadas(departamento) == resultado