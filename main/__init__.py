import os
from flask import Flask
from dotenv import load_dotenv
# modulo api rest
from flask_restful import Api
# modulo base de datos
from flask_sqlalchemy import SQLAlchemy

# importar el modulo jwt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

api = Api()

db = SQLAlchemy()

jwt = JWTManager()



def create_app():

  app = Flask(__name__)

  cors = CORS(app, resources = {r'/*': {'origins': '*'} })

  # cargar variables de entorno
  load_dotenv()
  
  # configuracion base de datos
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_ENGINE_OPTIONS'] ={
    "pool_pre_ping": True, 
    "pool_recycle": 300,
  }
  # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/negocioCesar"
  app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Goo3Ylm4pLdJENKgIyGU@containers-us-west-189.railway.app:6084/railway"

  db.init_app(app)

  # crear base de datos si no existe


  # importa el init de resources
  import main.resources as resources

  api.add_resource(resources.ProductoResource, '/producto/<detalle>')
  api.add_resource(resources.ProductosResource, '/productos')
  api.add_resource(resources.ComprasResource, '/compras')
  api.add_resource(resources.CompraResource, '/compra/<id_compra>')
  api.add_resource(resources.CompraFechaResource, '/compra/<fecha_compra>')
  api.add_resource(resources.UsuarioResource, '/usuario/<email>')
  api.add_resource(resources.UsuariosResource, '/usuarios')
  api.add_resource(resources.InventariosResource, '/inventarios')
  api.add_resource(resources.LocalsResource, '/locals')
  api.add_resource(resources.VentasResource, '/ventas')
  api.add_resource(resources.DetalleVentaResource, '/detalle_venta/<id_detalle_venta>')
  api.add_resource(resources.DetalleVentasResource, '/detalle_ventas')
  api.add_resource(resources.IntercambioResource, '/intercambio')

  # inicializa la api en app principal
  api.init_app(app)

  # configurar el jwt
  app.config['JWT_SECRET_KEY'] = "ejemplo123"
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(3600)

  jwt.init_app(app)

  from main.auth import routes
  app.register_blueprint(auth.routes.auth)

  return app