from .. import db

class Local(db.Model):
    __tablename__ = 'Local'
    id_local = db.Column(db.Integer, primary_key = True)
    detalle_local = db.Column(db.String(70), nullable = False)
    cantidad_local = db.Column(db.Integer, nullable = False)
    local_local = db.Column(db.Integer, nullable = False)
    ventas = db.relationship('Venta', back_populates = 'producto_local')

    def __repr__(self) -> str:
        return f'detalle_local : {self.detalle_local}'

    def to_json(self):
        local_json = {
            "id_local": self.id_local,
            "detalle_local": self.detalle_local,
            "cantidad_local": self.cantidad_local,
            "local_local": self.local_local
        }
        return local_json

    @staticmethod 
    def from_json(local_json):
        id_local = local_json.get("id_local")
        detalle_local = local_json.get("detalle_local")
        cantidad_local = local_json.get("cantidad_local")
        local_local = local_json.get("local_local")
        return Local(
            id_local = id_local,
            detalle_local = detalle_local,
            cantidad_local = cantidad_local,
            local_local = local_local
        )
