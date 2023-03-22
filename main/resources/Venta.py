from flask import request, jsonify
from flask_restful import Resource
from .. import db
from main.models import VentaModel, LocalModel, DetalleVentaModel


class Ventas(Resource):
    def get(self):
        ventas = db.session.query(VentaModel).all()
        return jsonify(
            {
               "ventas":  [venta.to_json() for venta in ventas]
            }
        )

    def post(self):
        venta = VentaModel.from_json(request.get_json())
        detalle_venta = request.get_json().get("detalle_venta")
        cantidad_venta = request.get_json().get("cantidad_venta")
        local_venta = request.get_json().get("local_venta")
        local = comprobarProductoLocal(detalle_venta, cantidad_venta, local_venta)
        try:
            if local:
                modificarLocalPorCompra(local, cantidad_venta)
                db.session.add(venta)
                db.session.commit()
                return venta.to_json(),201
            else:
                return {
                    "message": "no existe el producto o no hay suficientes productos",
                    "status": "error"
                },404
        except:
            return {
                "message": "ocurrio un error",
                "status": "error"
            },400
        finally:
            db.session.close()


def comprobarProductoLocal(detalle_venta, cantidad_venta, local_venta):
    local = db.session.query(LocalModel).filter(
        LocalModel.detalle_local == detalle_venta, 
        LocalModel.local_local == local_venta, 
        LocalModel.cantidad_local >= cantidad_venta
    ).first()
    if local:
        return local
    else:
        return False


def modificarLocalPorCompra( local, cantidad_venta):
    cantidad_total = local.cantidad_local - cantidad_venta
    setattr(local, "cantidad_local", cantidad_total)
    db.session.add(local)



