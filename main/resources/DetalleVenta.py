from flask import request, jsonify
from flask_restful import Resource
from main.models import DetalleVentaModel, VentaModel, LocalModel
from .. import db

class DetalleVenta(Resource):
    def delete(self, id_detalle_venta):
        id_venta = db.session.query(DetalleVentaModel).get(id_detalle_venta)
        try:
            modificarLocalPorVenta(id_detalle_venta)
            db.session.delete(id_venta)
            db.session.commit()
            return {
                "message": "se elimino con exito",
                "status": "ok"
            },200
        except:
            return{
                "message":"No se encontro la venta",
                "estatus": "error"
            },404

def modificarLocalPorVenta(id_venta):
    ventas = db.session.query(VentaModel).filter(VentaModel.id_detalle_venta == id_venta).all()
    for venta in ventas:
        devolucion = db.session.query(LocalModel).filter(
            LocalModel.detalle_local == venta.detalle_venta,
            LocalModel.local_local == venta.local_venta
            ).first()
        cantidad_total = venta.cantidad_venta + devolucion.cantidad_local
        setattr(devolucion, "cantidad_local", cantidad_total)
        db.session.add(devolucion)

class DetalleVentas(Resource):

    def post(self):
        id_detalle_venta = DetalleVentaModel.from_json(request.get_json())
        try:
            db.session.add(id_detalle_venta)
            db.session.commit()
            return id_detalle_venta.to_json()
        except:
            return {
                "message": "ocurrio un error",
                "status" : "error"
            }, 201