def valdatos(dni, nombre, apellido, numero):
    if len(str(dni)) != 8:
        return "El DNI es incorrecto"
    elif any(i.isnumeric() for i in nombre):
        return "El DNI es incorrecto"
    elif any(i.isnumeric() for i in apellido):
        return "Nombre contiene números"    
    elif len(str(numero)) != 9:
        return "Número contiene menos de 9 dígitos"
    else:
        return ""
    