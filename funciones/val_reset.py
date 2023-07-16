def valreset(user_id, new_password, confirm_password):
    if user_id is  None:
        return "No se encontró id de usuario."
    elif new_password != confirm_password:
        return "Contraseñas no coinciden."
    elif len(new_password) <8:
        return "Contraseña muy corta"
    elif new_password.isnumeric():
        return "Contraseña solo contiene números"
    else: 
        return ""