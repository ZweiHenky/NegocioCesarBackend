from flask import request, Blueprint
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import create_access_token
from main.auth.decorators import user_identity_lookup

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
  #Buscamos al usuario en la db mediante el mail
  usuario = db.session.query(UsuarioModel).filter(UsuarioModel.email == request.get_json().get('email')).first()
  #Validamos la contraseña de ese usuario
  try:
    if usuario.validate_password(request.get_json().get("password")):
      #Generamos un nuevo token y le pasamos al usuario como identidad de es token
      access_token = create_access_token(identity=usuario)
      #Devolvemos los valores y el token
      data = {
          'email': usuario.email,
          'nombre': usuario.nombre,
          'access_token': access_token,
          'role': str(usuario.role),
          'status': usuario.status,
          'local': usuario.local

      }
      return data, 200
    else:
      return {
        'messgae': 'Usuario o Contraseña incorrecta'
      }, 401
  except:
    db.session.rollback()
    return {
        'messgae': 'Error al iniciar sesion'
      }, 401

@auth.route('/register', methods=['POST'])
def register():
  usuario = UsuarioModel.from_json(request.get_json())
  exits = db.session.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).scalar() is not None
  if exits:
    return {
      "message": 'El correo ya esta en uso'
    }, 409
  else:
    try:
      db.session.add(usuario)
      db.session.commit()
    except Exception as error:
      db.session.rollback()
      return str(error), 409
    return usuario.to_json(), 201
    