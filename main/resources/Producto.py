from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel

class Producto(Resource):
    def get(self, detalle):
        productos = db.session.query(ProductoModel).filter(ProductoModel.nombre.like('%'+detalle+'%')).all() 
        try:
            if(productos == []):
                return {
                    "message": "No hay ningun producto con ese nombre"
                }, 404
            else:
                return jsonify(
                    {
                        'producto': [producto.to_json() for producto in productos]
                    }
                )
        except:
            return {
                "message": "Error"
            }, 404

    

    def delete(self, detalle):
        producto = db.session.query(ProductoModel).get(detalle)
        try:
            db.session.delete(producto)
            db.session.commit()
            return {
                "message": "se elimino con exito",
                "status": "ok"
            }, 201
        except:
            return {
                "message": "ocurrio un error al intentar eliminarlo",
                "status": "error"
            }, 404

    def put(self, detalle):
        producto = db.session.query(ProductoModel).get(detalle)
        data = request.get_json().items()
        for key, value in data:
            setattr(producto, key, value)
        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json()
        except:
            db.session.rollback()
            return {'message':'error en la actualizacion'}, 404

class Productos(Resource):
    def get(self):
        try:
            productos = db.session.query(ProductoModel).all()
            return jsonify(
                {
                    'producto': [producto.to_json() for producto in productos]
                }
            )
        except:
            db.session.rollback()
            return 404
        
    def post(self):
        producto = ProductoModel.from_json(request.get_json())
        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        except:
            db.session.rollback()
            return {
                'message' : 'el producto ya existe'
            }, 400
