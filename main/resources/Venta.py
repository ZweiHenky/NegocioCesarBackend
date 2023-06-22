from flask import request, jsonify
from flask_restful import Resource
from .. import db
from main.models import VentaModel, LocalModel, DetalleVentaModel

class Venta(Resource):
    def get(self, fecha_venta):
        ventas = db.session.query(VentaModel).filter(VentaModel.fecha_venta.like('%'+fecha_venta+'%')).all()
        try:
            if(ventas == []):
                return {
                    "message": "No hay compras con esa fecha"
                }, 404
            else:
                return jsonify(
                    {
                        'ventas': [venta.to_json() for venta in ventas]
                    }
                )
        except:
            return {
                "message": "Error"
            }, 404
        finally:
            db.session.close()

class Ventas(Resource):
    def get(self):
        ventas = db.session.query(VentaModel).all()
        return jsonify(
            {
               "ventas":  [venta.to_json() for venta in ventas]
            }
        )

    def post(self):
        requestSend = request.get_json()
        responseVentas = []
        try:
            for ventaRequest in requestSend :
                venta = VentaModel.from_json(ventaRequest)
                detalle_venta = ventaRequest['detalle_venta']
                cantidad_venta = ventaRequest['cantidad_venta']
                local_venta = ventaRequest['local_venta']
                local = comprobarProductoLocal(detalle_venta, cantidad_venta, local_venta)

                if local:
                    # modificarLocalPorCompra(local, cantidad_venta)
                    db.session.add(venta)
                    responseVentas.append(ventaRequest)
                else:
                    return {
                        "message": "no existe el producto o no hay suficientes productos",
                        "status": "error"
                    },404
            
            db.session.commit()
            return{
                'message': 'se realizo con exito',
                'ventas' : responseVentas
            }
        except Exception as e:
            print(e)
            return {
                "message": "ocurrio un error",
                "status": "error"
            },400
        finally:
            db.session.close()


def comprobarProductoLocal(detalle_venta, cantidad_venta, local_venta):
    local = db.session.query(LocalModel).get(detalle_venta)
    local = db.session.query(LocalModel).filter(
        LocalModel.id_local == detalle_venta, 
        LocalModel.local_local == local_venta, 
        LocalModel.cantidad_local >= cantidad_venta
    ).first()
    print(local)
    if local:
        return local
    else:
        return False


def modificarLocalPorCompra( local, cantidad_venta):
    cantidad_total = local.cantidad_local - cantidad_venta
    setattr(local, "cantidad_local", cantidad_total)
    db.session.add(local)



