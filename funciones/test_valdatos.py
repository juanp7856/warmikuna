import pytest

from funciones.val_datos import valdatos


@pytest.mark.parametrize(
    "dni, nombre, apellido,numero,resultado",
    [
        (87654321, "nombre", "apellido", 987654321, ""), #ESCENARIO ACERTADO
        (87654321, "n1e", "al2do", 987654321, ""), #ESCENARIO ERRÓNEO
        (87, "nombre", "apellido", 987654321, ""), #ESCENARIO ERRÓNEO
        (871, "nombre", "apellido", 987654321, "El DNI es incorrecto") #ESCENARIO ACERTADO
    ]
)
def test_val_datos(dni, nombre, apellido, numero, resultado):
    assert valdatos(dni, nombre, apellido, numero) == resultado