from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModel, InventarioModel, ProductoModel

class Compra(Resource):

    def delete(self, id_compra):
        compra = db.session.query(CompraModel).get(id_compra)
        try:
            ModificarInventarioPorEliminacion(compra)
            db.session.delete(compra)
            db.session.commit()
            return {
                "message": "se elimino con exito"
            }, 201
        except:
            return{
                "message": "ocurrio un error, vuelva a intentarlo"
            }, 404
        finally:
            db.session.close()

    def put(self, id_compra):
        compra = db.session.query(CompraModel).get_or_404(id_compra)
        data = request.get_json().items()
        for key, value in data:
            setattr(compra, key, value)
        try:
            db.session.add(compra)
            db.session.commit()
        except:
            return {
                'message':'Ocurrio Un problema'
            },404
        finally:
            db.session.close()

    

class CompraFecha(Resource):
    def get(self, fecha_compra):
        compras = db.session.query(CompraModel).filter(CompraModel.fecha_compra.like('%'+fecha_compra+'%')).all()
        try:
            if(compras == []):
                return {
                    "message": "No hay compras con esa fecha"
                }, 404
            else:
                return jsonify(
                    {
                        'compra': [compra.to_json() for compra in compras]
                    }
                )
        except:
            return {
                "message": "Error"
            }, 404
        finally:
            db.session.close()

class Compras(Resource):

    def post(self):
        compra = CompraModel.from_json(request.get_json())
        detalle_compra = db.session.query(ProductoModel).filter(ProductoModel.detalle == request.get_json().get('detalle_producto_compra')).first()
        if detalle_compra is not None:
            try:
                modificarInventario(request.get_json())
                db.session.add(compra)
                db.session.commit()
                return compra.to_json(), 201
            except: 
                return {
                    "message": "ocurrio un problema"
                }, 404
            finally:
                db.session.close()
        else:
            return{
                "message": "No existe ese producto"
            }, 404
        

        
    def get(self):
        compras = db.session.query(CompraModel).all()

        return jsonify(
            {
                'compras' : [compra.to_json() for compra in compras]
            }
        )
        
def modificarInventario(inventario_json):
    inventario = db.session.query(InventarioModel).filter(InventarioModel.detalle_inventario == inventario_json.get("detalle_producto_compra")).first()
    
    if inventario is None:
        inventario = InventarioModel.from_json(inventario_json)
        db.session.add(inventario)
    else:
        detalle_inventario = inventario_json.get("detalle_producto_compra")
        cantidad_inventario = inventario_json.get("cantidad_compra")
        cantidad_total = inventario.cantidad_inventario + cantidad_inventario
        setattr(inventario, "detalle_inventario", detalle_inventario)
        setattr(inventario, "cantidad_inventario", cantidad_total)
        db.session.add(inventario)

def ModificarInventarioPorEliminacion(compra):
    detalle = compra.detalle_producto_compra
    inventario = db.session.query(InventarioModel).filter(InventarioModel.detalle_inventario == detalle).first()
    cantidad_total = inventario.cantidad_inventario - compra.cantidad_compra
    setattr(inventario, 'cantidad_inventario', cantidad_total)
    db.session.add(inventario)
