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
        finally:
            db.session.close()

    

    def delete(self, detalle):
        producto = db.session.query(ProductoModel).get(detalle)
        try:
            db.session.delete(producto)
            db.session.commit()
            return {
                "message": "se elimino con exito"
            }, 201
        except:
            return {
                "message": "erro al eliminarlo"
            }, 404
        finally:
            db.session.close()

    def put(self, detalle):
        producto = db.session.query(ProductoModel).get(detalle)
        data = request.get_json().items()
        for key, value in data:
            setattr(producto, key, value)
        try:
            db.session.add(producto)
            db.session.commit()
            return {
                'message':'se actualizo con exito'
            }
        except:
            db.session.rollback()
            return {
                'message':'error en la actualizacion'
            }, 404
        finally:
            db.session.close()

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
        finally:
            db.session.close()
        
    def post(self):
        producto = ProductoModel.from_json(request.get_json())
        try:
            db.session.add(producto)
            db.session.commit()
            return {
                'message': 'se realizo con exito',
                'producto' : producto.to_json(),
            }, 201
        except:
            db.session.rollback()
            return {
                'message' : 'el producto ya existe'
            }, 400
        finally:
            db.session.close()
