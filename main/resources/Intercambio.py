from flask import request, jsonify
from flask_restful import Resource
from main.models import LocalModel
from .. import db

class Intercambio(Resource):
    def put(self):
        req = request.get_json()
        local1 = req["intercambio"][0]
        local2 = req["intercambio"][1]

        producto1 = db.session.query(LocalModel).filter(LocalModel.id_local == local1["id_local"]).first()
        producto2 = db.session.query(LocalModel).filter(LocalModel.id_local == local2["id_local"]).first()
        
        comprobacion_local1 = db.session.query(LocalModel).filter(
            LocalModel.detalle_local == producto1.detalle_local,
            LocalModel.local_local == producto2.local_local
            ).first()
        comprobacion_local2 = db.session.query(LocalModel).filter(
            LocalModel.detalle_local == producto2.detalle_local,
            LocalModel.local_local == producto1.local_local
            ).first()

        try:
            if comprobacion_local1 is None:
                setattr(producto1, "cantidad_local", producto1.cantidad_local-1)
                db.session.add(producto1)
                nuevo_producto1 = LocalModel(id_local = None, detalle_local = producto2.detalle_local, cantidad_local = 1 , local_local = 2)
                db.session.add(nuevo_producto1)
                if comprobacion_local2 is None:
                    setattr(producto2, "cantidad_local", producto2.cantidad_local-1)
                    db.session.add(producto2)
                    nuevo_producto2 = LocalModel(id_local = None, detalle_local = producto2.detalle_local, cantidad_local = 1 , local_local = 1)
                    db.session.add(nuevo_producto2)
                else:
                    setattr(producto2, "cantidad_local", producto2.cantidad_local-1)
                    setattr(comprobacion_local2, "cantidad_local", comprobacion_local2.cantidad_local + 1)
                    db.session.add(producto2)
                    db.session.add(comprobacion_local2)
            else:
                setattr(comprobacion_local1, "cantidad_local", comprobacion_local1.cantidad_local + 1)
                setattr(producto1, "cantidad_local", producto1.cantidad_local-1) 
                db.session.add(comprobacion_local1)
                db.session.add(producto1)
                if comprobacion_local2 is None:
                    setattr(producto2, "cantidad_local", producto2.cantidad_local-1)
                    db.session.add(producto2)
                    nuevo_producto2 = LocalModel(id_local = None, detalle_local = producto2.detalle_local, cantidad_local = 1 , local_local = 1)
                    db.session.add(nuevo_producto2)
                else:
                    setattr(producto2, "cantidad_local", producto2.cantidad_local-1)
                    setattr(comprobacion_local2, "cantidad_local", comprobacion_local2.cantidad_local + 1)
                    db.session.add(producto2)
                    db.session.add(comprobacion_local2)    
            db.session.commit()
        except:
            return {
                'message':'Ocurrio un error'
            }
        finally:
            db.session.close()
        

