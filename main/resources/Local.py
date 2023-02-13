from flask import request, jsonify
from flask_restful import Resource
from main.models import LocalModel, InventarioModel
from .. import db

def modificarInventarioALocal(inventario, cantidad_local, estado_local):
    if estado_local == "devolver":
        cantidad_total = inventario.cantidad_inventario + cantidad_local
    if estado_local == "agregar":
        cantidad_total = inventario.cantidad_inventario - cantidad_local
    estado = True
    if cantidad_total >= 1:
        setattr(inventario, "detalle_inventario", inventario.detalle_inventario)
        setattr(inventario, "cantidad_inventario", cantidad_total)
        estado = True
        return inventario, estado
    else:
        estado = False
        return inventario, estado


class Locals(Resource):

    def get(self):
        productos = db.session.query(LocalModel).all()
        return jsonify(
            {
                "productos":[producto.to_json() for producto in productos]
            }
        )

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
                    return local.to_json(), 201
                else:
                    return {
                        "message": "no hay suficientes productos en el inventario",
                        "error": "error"
                    },404
            except:
                return {
                    "message": "error al agregar el producto",
                    "status": "error"
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
                        return local.to_json(), 201
                    else:
                        return {
                            "message": "no hay suficientes productos en el local",
                            "error": "error"
                        },404
                else:
                    return {
                        "message": "no hay suficientes productos en el inventario",
                        "error": "error"
                    },404
            except:
                return {
                    "message": "error al agregar el producto",
                    "status": "error"
                },404
