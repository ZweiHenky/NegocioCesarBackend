from .. import db

class DetalleVenta(db.Model):
    __tablename__ = 'DetalleVenta'
    id_detalle_venta = db.Column(db.Integer, primary_key = True)
    detalle_ventas = db.relationship('Venta', back_populates = 'detalle_venta_venta', cascade = 'all, delete-orphan')

    def to_json(self):
        detalle_venta = {
            "id_detalle_venta" : self.id_detalle_venta
        }
        return detalle_venta
    
    @staticmethod
    def from_json(detalle_venta_json):
        id_detalle_venta = detalle_venta_json.get("id_detalle_venta")
        return DetalleVenta(id_detalle_venta = id_detalle_venta)