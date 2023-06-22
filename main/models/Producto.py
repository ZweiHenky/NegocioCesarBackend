from .. import db

class Producto(db.Model):
    __tablename__ = 'Producto'
    detalle = db.Column(db.String(70), primary_key = True)
    nombre = db.Column(db.String(40), nullable = False)
    color = db.Column(db.String(10), nullable = False)
    talla = db.Column(db.String(5), nullable = False)
    venta = db.Column(db.Integer, nullable = False)
    compra = db.Column(db.Integer, nullable = False)
    compras = db.relationship('Compra', back_populates = 'producto')
    # ventas = db.relationship('Venta', back_populates = 'producto')

    def __repr__(self):
        return f'Producto:{self.nombre}'

    def to_json(self):
        producto_json = {
            'detalle': self.detalle,
            'nombre': self.nombre,
            'color': self.color,
            'talla': self.talla,
            'venta': self.venta,
            'compra': self.compra
        }
        return producto_json
    
    @staticmethod
    def from_json(producto_json):
        detalle = producto_json.get("detalle"),
        nombre = producto_json.get("nombre"),
        color = producto_json.get("color"),
        talla = producto_json.get("talla"),
        venta = producto_json.get("venta"),
        compra = producto_json.get("compra")
        

        return Producto(
            detalle = detalle,
            nombre = nombre,
            color = color,
            talla = talla,
            venta = venta,
            compra = compra
        )
