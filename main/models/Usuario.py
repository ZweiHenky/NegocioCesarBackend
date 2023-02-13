from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    email = db.Column(db.String(80), nullable = False, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(300), nullable = False)
    role = db.Column(db.String(20), nullable = False, default = 'vendedor')
    status = db.Column(db.Boolean, nullable = False, default = False)
    ventas_usuario = db.relationship('Venta', back_populates = 'usuario')

    def __repr__(self) -> str:
        return f'{self.email}'

    @property
    def plain_password(self):
        raise AttributeError('La contraseña no se puede leer')

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        usuario_json = {
            "email": self.email,
            "nombre": self.nombre,
            "role": self.role,
            "status": self.status
        }
        return usuario_json
    
    @staticmethod
    def from_json(usuario_json):
        email = usuario_json.get("email")
        nombre = usuario_json.get("nombre")
        password = usuario_json.get("password")
        role = usuario_json.get("rol")
        status = usuario_json.get("status")

        return Usuario(
            email = email,
            nombre = nombre,
            plain_password = password,
            role = role,
            status = status
        )