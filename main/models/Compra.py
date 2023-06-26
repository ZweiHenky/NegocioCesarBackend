from .. import db
import datetime as dt

class Compra(db.Model):
    __tablename__ = 'Compra'
    id_compra = db.Column(db.Integer, primary_key = True)
    cantidad_compra = db.Column(db.Integer, nullable = False)
    fecha_compra = db.Column(db.DateTime, default=dt.utcnow, nullable = False)
    detalle_producto_compra = db.Column(db.String(70), db.ForeignKey('Producto.detalle'), nullable = True)
    producto = db.relationship('Producto', back_populates = 'compras', uselist = False)

    def __repre__(self):
        return f'Compra: {self.detalle_producto_compra}'

    def to_json(self):
        if self.producto is None:
            compra_json = {
                'id_compra': self.id_compra,
                'cantidad_compra': self.cantidad_compra,
                'fecha_compra': str(self.fecha_compra),
                'producto': "el producto ha sido eliminado"
            }
        else:
            compra_json = {
                'id_compra': self.id_compra,
                'cantidad_compra': self.cantidad_compra,
                'fecha_compra': str(self.fecha_compra),
                'producto': self.producto.to_json()
            }

        return compra_json

    @staticmethod
    def from_json(compra_json):
        id_compra = compra_json.get('id_compra')
        cantidad_compra = compra_json.get('cantidad_compra')
        fecha_compra = compra_json.get('fecha_compra')
        detalle_producto_compra = compra_json.get('detalle_producto_compra')

        return Compra(
            id_compra = id_compra,
            cantidad_compra = cantidad_compra,
            fecha_compra = fecha_compra,
            detalle_producto_compra = detalle_producto_compra
        )