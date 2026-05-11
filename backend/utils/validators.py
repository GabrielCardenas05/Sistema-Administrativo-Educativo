# Validadores
# Funciones para validar datos de entrada

import re

def validar_correo(correo):
    """Valida el formato de un correo electrónico"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None

def validar_contraseña(contraseña):
    """Valida que la contraseña cumpla con los requisitos de seguridad"""
    # Al menos 8 caracteres, una mayúscula, una minúscula, un número
    if len(contraseña) < 8:
        return False
    if not re.search(r'[A-Z]', contraseña):
        return False
    if not re.search(r'[a-z]', contraseña):
        return False
    if not re.search(r'[0-9]', contraseña):
        return False
    return True

def validar_matricula(matricula):
    """Valida el formato de una matrícula"""
    pass

def validar_no_vacio(valor):
    """Valida que un valor no esté vacío"""
    return valor is not None and str(valor).strip() != ""

def validar_numero(valor):
    """Valida que un valor sea un número"""
    try:
        float(valor)
        return True
    except (ValueError, TypeError):
        return False
