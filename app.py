from flask import Flask, render_template, request, flash, redirect, url_for, session
from application.controllers.ProductosController import ProductosController
from application.controllers.UsuariosController import UsuariosController
from application.db.DBConnection import DBConnection

app = Flask(__name__)
app.secret_key = 'alguna_clave_secreta_y_dificil_de_adivinar'

class ArubaStoreApp:
    def __init__(self, app):
        self.app = app
        self.db_connection = DBConnection(self.app)
        # Creación de la instancia del controlador de productos
        self.productos_controller = ProductosController(app, self.db_connection)
        self.usuarios_controller = UsuariosController(app, self.db_connection)

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

app.add_url_rule('/', 'index', aruba_app.index)
app.add_url_rule('/contacto', 'contacto', aruba_app.contacto)
app.add_url_rule('/nosotros', 'nosotros', aruba_app.nosotros)
app.add_url_rule('/pagUsuario', 'pagUsuario', aruba_app.pag_usuario)
app.add_url_rule('/register', 'register', aruba_app.register)
app.add_url_rule('/carrito', 'carrito', aruba_app.carrito)

if __name__ == '__main__':
    aruba_app.run()