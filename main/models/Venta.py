from .. import db
import datetime as dt
import pytz

class Venta(db.Model):
    __tablename__ = 'Venta'
    id = db.Column(db.Integer, primary_key = True)
    local_venta = db.Column(db.Integer, nullable = False)
    cantidad_venta = db.Column(db.Integer, nullable = False)
    metodo_pago_venta = db.Column(db.String(20), nullable = False)
    otro_precio = db.Column(db.Integer, nullable = True)
    fecha_venta = db.Column(db.DateTime, default = dt.utcnow, nullable = False)
    # detalle venta local es el id de cada producto de la clase local
    detalle_venta = db.Column(db.Integer, db.ForeignKey('Local.id_local'), nullable = True )
    producto_local = db.relationship('Local', back_populates = 'ventas', uselist = False)
    usuario_venta = db.Column(db.String(80), db.ForeignKey('Usuario.email'), nullable = True)
    usuario = db.relationship('Usuario', back_populates = 'ventas_usuario', uselist = False)
    id_detalle_venta = db.Column(db.Integer, db.ForeignKey('DetalleVenta.id_detalle_venta'), nullable = False)
    detalle_venta_venta = db.relationship('DetalleVenta', back_populates = 'detalle_ventas', uselist = False)

    # db.DateTime(timezone=True), server_default=func.now()

    def __repr__(self) -> str:
        return f'{self.detalle_venta}'

    def to_json(self):

        if self.producto_local is None:
            venta_json = {
                "id": self.id,
                "local_venta": self.local_venta,
                "cantidad_venta": self.cantidad_venta,
                "metodo_pago_venta": self.metodo_pago_venta,
                "otro_precio": self.otro_precio,
                "fecha_venta": str(self.fecha_venta),
                "producto_local": "el producto se ha eliminado",
                "usuario": self.usuario.to_json(),
                "detalle_venta_venta": self.detalle_venta_venta.to_json()
            }
        else:
            venta_json = {
                "id": self.id,
                "local_venta": self.local_venta,
                "cantidad_venta": self.cantidad_venta,
                "metodo_pago_venta": self.metodo_pago_venta,
                "otro_precio": self.otro_precio,
                "fecha_venta": str(self.fecha_venta),
                "producto_local": self.producto_local.to_json(),
                "usuario": self.usuario.to_json(),
                "detalle_venta_venta": self.detalle_venta_venta.to_json()
            }
        return venta_json
    
    @staticmethod
    def from_json(venta_json):
        id = venta_json.get('id')
        local_venta = venta_json.get('local_venta')
        cantidad_venta = venta_json.get('cantidad_venta')
        metodo_pago_venta = venta_json.get('metodo_pago_venta')
        otro_precio = venta_json.get('otro_precio')
        fecha_venta = venta_json.get('fecha_venta')
        detalle_venta = venta_json.get('detalle_venta')
        usuario_venta = venta_json.get('usuario_venta')
        id_detalle_venta = venta_json.get('id_detalle_venta')

        return Venta(
            id = id,
            local_venta = local_venta,
            cantidad_venta = cantidad_venta,
            metodo_pago_venta = metodo_pago_venta,
            otro_precio = otro_precio,
            fecha_venta = fecha_venta,
            detalle_venta = detalle_venta,
            usuario_venta = usuario_venta,
            id_detalle_venta = id_detalle_venta
        )
