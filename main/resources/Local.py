from flask import request, jsonify
from flask_restful import Resource
from main.models import LocalModel, InventarioModel
from .. import db

class Locals(Resource):

    def get(self):
        productos = db.session.query(LocalModel).all()
        try:
            return jsonify(
                {
                    "productos":[producto.to_json() for producto in productos]
                }
            )
        except:
            return{
                'message':'Ocurrio un error'
            }
        finally:
            db.session.close()

    def put(self):
        local = db.session.query(LocalModel).filter(
            LocalModel.detalle_local == request.get_json().get("detalle_local"),
            LocalModel.local_local == request.get_json().get("local_local")
        ).first()
        inventario = db.session.query(InventarioModel).filter(
            InventarioModel.detalle_inventario == request.get_json().get("detalle_local")
        ).first()
        cantidad_local = request.get_json().get('cantidad_local')
        estado_local = request.get_json().get('estado')
        data = request.get_json().items()
        if local is None:
            local = LocalModel.from_json(request.get_json())
            try:
                nuevo_inventario, estado = modificarInventarioALocal(inventario, cantidad_local, estado_local)
                if estado:
                    db.session.add(nuevo_inventario)
                    db.session.add(local)
                    db.session.commit()
                    return {
                            "message": 'se realizo con exito',
                            "producto" : local.to_json(),
                            "estado" : estado_local
                        }, 201
                else:
                    return {
                        "message": "no hay suficientes productos en el inventario"
                    },404
            except:
                return {
                    "message": "error al agregar el producto"
                }
        else:
            for key, value in data:
                if key == "cantidad_local" :
                    if estado_local == "devolver":
                        cantidad_total_local = local.cantidad_local - value
                    if estado_local == "agregar":
                        cantidad_total_local = value + local.cantidad_local
                    setattr(local, key, cantidad_total_local)
                else:
                    setattr(local, key, value)
            try:
                nuevo_inventario, estado = modificarInventarioALocal(inventario, cantidad_local, estado_local)
                if estado:
                    if cantidad_total_local >= 1:
                        db.session.add(nuevo_inventario)
                        db.session.add(local)
                        db.session.commit()
                        return {
                            "message": 'se realizo con exito',
                            "producto" : local.to_json(),
                            "estado" : estado_local
                        }, 201
                    else:
                        return {
                            "message": "no hay suficientes productos en el local"
                        },404
                else:
                    return {
                        "message": "no hay suficientes productos en el inventario"
                    },404
            except:
                return {
                    "message": "error al agregar el producto"
                },404
            finally:
                db.session.close()


def modificarInventarioALocal(inventario, cantidad_local, estado_local):
    if estado_local == "devolver":
        cantidad_total = inventario.cantidad_inventario + cantidad_local
    if estado_local == "agregar":
        cantidad_total = inventario.cantidad_inventario - cantidad_local
    estado = True
    if cantidad_total >= 0:
        setattr(inventario, "detalle_inventario", inventario.detalle_inventario)
        setattr(inventario, "cantidad_inventario", cantidad_total)
        estado = True
        return inventario, estado
    else:
        estado = False
        return inventario, estado