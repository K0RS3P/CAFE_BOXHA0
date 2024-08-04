
import json


class Usuario:
    def __init__(self, nombre, apellido, email, rol, password):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.rol = rol
        self.password = password

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'rol': self.rol,
            'password': self.password
        }

    def __str__(self):
        return f"{self.nombre} ({self.rol})"
    
    @staticmethod
    def validar_nombre(nombre):
        import re
        pattern = r'^[A-Za-z\s]+$'
        return bool(re.match(pattern, nombre))
    
    @staticmethod
    def validar_apellido(apellido):
        import re
        pattern = r'^[A-Za-z\s]+$'
        return bool(re.match(pattern, apellido))

    @staticmethod
    def validar_email(email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    @staticmethod
    def validar_password(password):
        if len(password) < 6:
            return False
        return True

