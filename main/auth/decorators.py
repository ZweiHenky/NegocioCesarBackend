from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles):
  def decorator(function):
    def wrapper(*args, **kwargs):
      # verificar si es correcto el jwt
      verify_jwt_in_request()
      # obtenemos los claims (peticiones)
      claims = get_jwt()
      if claims['sub']['role'] in roles:
        return function(*args, **kwargs)
      else:
        return 'Rol not allowed', 403
    return wrapper
  return decorator

@jwt.user_identity_loader
def user_identity_lookup(usuario):
  return {
    'email': usuario.email,
    'nombre': usuario.nombre,
    'role': usuario.role,
    'local': usuario.local,
    'status':usuario.status
  }

@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
  claims = {
    'role': usuario.role,
    'email': usuario.email,
    'nombre':usuario.nombre,
    'local': usuario.local,
    'status':usuario.status
  }