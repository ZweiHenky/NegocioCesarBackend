from flask import request, jsonify
from flask_restful import Resource
from .. import db
from main.models import InventarioModel


class Inventarios(Resource):
    
    def get(self):
        inventarios = db.session.query(InventarioModel).all()
        return jsonify(
            {
                "inventario": [inventario.to_json() for inventario in inventarios]
            }
        )