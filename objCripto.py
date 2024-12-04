from cryptography.fernet import Fernet

class Cripto:
    def __init__(self, password):
        self.Criptword = password

    def generar_clave(self):
        clave = Fernet.generate_key()
        with open("Cache/clave.key", "wb") as archivo_clave:
            archivo_clave.write(clave)

    def cargar_clave(self):
        with open("Cache/clave.key", "rb") as archivo_clave:
            return archivo_clave.read()

    def cifrar_contraseña(self):
        clave = self.cargar_clave()
        fernet = Fernet(clave)
        return fernet.encrypt(self.Criptword.encode())

    def descifrar_contraseña(self):
        clave = self.cargar_clave()
        fernet = Fernet(clave)
        return fernet.decrypt(self.Criptword).decode()




