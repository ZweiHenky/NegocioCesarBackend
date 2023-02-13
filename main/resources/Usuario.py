from .. import db
from flask_restful import Resource
from flask import request, jsonify
from main.models import UsuarioModel

class Usuario(Resource):

    def get(self, email):
        usuario = db.session.query(UsuarioModel).get_or_404(email)
        return usuario.to_json()

    def put(self, email):
        usuario = db.session.query(UsuarioModel).get(email)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(),201
        except:
            return {
                "message":"ocurrio un error al intentar actualizar el usuairo",
                "status": "error"
            },505


    def delete(self, email):
        usuario = db.session.query(UsuarioModel).get(email)
        try:
            db.session.delete(usuario)
            db.session.commit()
            return {
                "message": "El usuario se elimino con exito",
                "status": "ok"
            }
        except:
            return {
                "message": "No se encontro el usuario",
                "status": "error"
            },404

class Usuarios(Resource):

    def get(self):
        usuarios = db.session.query(UsuarioModel).all()
        return jsonify(
            {
                "usuarios": [usuario.to_json() for usuario in usuarios]
            }
        )