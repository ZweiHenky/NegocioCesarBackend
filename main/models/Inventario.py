from .. import db

class Inventario(db.Model):
    __tablename__ = 'Inventario'
    id_inventario = db.Column(db.Integer, primary_key=True)
    detalle_inventario = db.Column(db.String(70), nullable = False, unique = True)
    cantidad_inventario = db.Column(db.Integer, nullable = False)

    def to_json(self):

        inventario_json = {
            "id_inventario": self.id_inventario,
            "detalle_inventario": self.detalle_inventario,
            "cantidad_inventario": self.cantidad_inventario
        }

        return inventario_json

    @staticmethod
    def from_json(inventario_json):
        
        id_inventario = inventario_json.get("id_inventario")
        detalle_inventario = inventario_json.get("detalle_producto_compra")
        cantidad_inventario = inventario_json.get("cantidad_compra")
        return Inventario(
            id_inventario = id_inventario,
            detalle_inventario = detalle_inventario,
            cantidad_inventario = cantidad_inventario
        ) 