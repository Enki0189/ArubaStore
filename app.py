from flask import Flask, render_template, request, flash, redirect, url_for, session
from application.controllers.PagosController import PagosController
from application.controllers.ProductosController import ProductosController
from application.controllers.UsuariosController import UsuariosController
from application.db.DBConnection import DBConnection
from application.db.dao.ProductosDao import ProductosDao
from application.domain.Cajero import Cajero
from application.domain.Deposito import Deposito
from application.domain.MedioDePago import Efectivo, MercadoPago, Tarjeta
from application.domain.Tienda import Tienda

app = Flask(__name__)
app.secret_key = 'alguna_clave_secreta_y_dificil_de_adivinar'

class ArubaStoreApp:
    def __init__(self, app):
        self.app = app
        self.db_connection = DBConnection(self.app)
        # Creación de la instancia del controlador de productos
        self.productos_controller = ProductosController(app, self.db_connection)
        self.usuarios_controller = UsuariosController(app, self.db_connection)
        self.pagos_controller = PagosController(app)
        productos_dao = ProductosDao(self.db_connection)
        deposito = Deposito(productos_dao)
        medios_pago = []
        medios_pago.append(MercadoPago())
        medios_pago.append(Tarjeta())
        medios_pago.append(Efectivo())
        cajero = Cajero(medios_pago)
        self.tienda = Tienda(cajero, deposito)
        self.register_routes()
    
    def register_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/contacto', 'contacto', self.contacto)
        self.app.add_url_rule('/nosotros', 'nosotros', self.nosotros)
        self.app.add_url_rule('/pagUsuario', 'pagUsuario', self.pag_usuario)
        self.app.add_url_rule('/register', 'register', self.register)
        self.app.add_url_rule('/carrito', 'carrito', self.carrito)

    def run(self):
        self.app.run(port=3000, debug=True)

    def index(self):
        print('Cargando pagina principal')
        return render_template("index.html")

    def contacto(self):
        return render_template("contacto.html")

    def nosotros(self):
        return render_template("nosotros.html")

    def pag_usuario(self):
        return render_template("pagUsuario.html")

    def register(self):
        return render_template("register.html")

    def carrito(self):
        return render_template("carrito.html")

aruba_app = ArubaStoreApp(app)

if __name__ == '__main__':
    aruba_app.run()