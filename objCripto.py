from cryptography.fernet import Fernet

def generar_clave():
    clave = Fernet.generate_key()
    with open("Cache/clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

def cargar_clave():
    with open("Cache/clave.key", "rb") as archivo_clave:
        return archivo_clave.read()

def cifrar_contraseña(contraseña):
    clave = cargar_clave()
    fernet = Fernet(clave)
    return fernet.encrypt(contraseña.encode())

def descifrar_contraseña(contraseña_cifrada):
    clave = cargar_clave()
    fernet = Fernet(clave)
    return fernet.decrypt(contraseña_cifrada).decode()