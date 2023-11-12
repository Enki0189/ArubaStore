from flask import Flask, render_template, request, flash, redirect, url_for, session
from application.controllers.ProductosController import ProductosController
from application.db.DBConnection import DBConnection

app = Flask(__name__)
app.secret_key = 'alguna_clave_secreta_y_dificil_de_adivinar'

class ArubaStoreApp:
    def __init__(self, app):
        self.app = app
        self.db_connection = DBConnection(self.app)
        self.mysql = self.db_connection.mysql
        # Creación de la instancia del controlador de productos
        self.productos_controller = ProductosController(app, self.mysql)

    def run(self):
        self.app.run(port=3000, debug=True)

    def index(self):
        print('Cargando pagina principal')
        return render_template("index.html")

    def contacto(self):
        return render_template("contacto.html")

    def nosotros(self):
        return render_template("nosotros.html")

    def pagUsuario(self):
        return render_template("pagUsuario.html")

    def login(self):
        return render_template("login.html")

    def register(self):
        return render_template("register.html")

    def carrito(self):
        return render_template("carrito.html")

    def crearUsuario(self):
        print('Se recibe solicitud de creación de nuevo usuario.')
        nombreUsuario = request.form['userName']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['phone']
        direccion = request.form['address']
        provincia = request.form['province']
        nombreYapellido = nombre + ' ' + apellido
        personalId = request.form['personalId']
        rol = 1

        try:
            cur = self.mysql.connection.cursor()
            cur.execute('INSERT INTO usuario (nombreUsuario, contraseña, rol, email, direccion, telefono, nombreYapellido, cuil, provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (nombreUsuario, password, rol, email, direccion, telefono, nombreYapellido, personalId, provincia))
            self.mysql.connection.commit()
            flash('Usuario creado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            self.mysql.connection.rollback()
            print(f"Error: {e}")
            flash('Hubo un error al crear el usuario. Por favor intenta nuevamente.', 'danger')

        return redirect(url_for('register'))

    def usuarioLogin(self):
        email = request.form['email']
        password = request.form['password']

        try:
            cur = self.mysql.connection.cursor()
            cur.execute('SELECT U.email, U.contraseña, R.descripcion FROM usuario U JOIN roles R ON U.rol = R.idRoles WHERE email = %s', [email])
            user = cur.fetchone()
            if user and user[1] == password:  # Aquí simplemente se compara directamente, pero deberías usar hashing.
                session['logged_in'] = True
                session['user_email'] = email
                session['tipo_usuario'] = user[2]
                flash('Inicio de sesión correcto.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Usuario y/o contraseñas incorrectos. Por favor intenta nuevamente.', 'danger')
        except Exception as e:
            print(f"Error: {e}")
            flash('Hubo un error al intentar iniciar sesión. Por favor intenta nuevamente.', 'danger')

        return redirect(url_for('login'))

    def logout(self):
        session.pop('logged_in', None)
        session.pop('user_email', None)
        session.pop('tipo_usuario', None)
        flash('Has cerrado sesión.', 'success')
        return redirect(url_for('index'))

aruba_app = ArubaStoreApp(app)

app.add_url_rule('/', 'index', aruba_app.index)
app.add_url_rule('/contacto', 'contacto', aruba_app.contacto)
app.add_url_rule('/nosotros', 'nosotros', aruba_app.nosotros)
app.add_url_rule('/pagUsuario', 'pagUsuario', aruba_app.pagUsuario)
app.add_url_rule('/login', 'login', aruba_app.login)
app.add_url_rule('/register', 'register', aruba_app.register)
app.add_url_rule('/carrito', 'carrito', aruba_app.carrito)
app.add_url_rule('/usuario', 'crearUsuario', aruba_app.crearUsuario, methods=['POST'])
app.add_url_rule('/usuario/login', 'usuarioLogin', aruba_app.usuarioLogin, methods=['POST'])
app.add_url_rule('/logout', 'logout', aruba_app.logout)


if __name__ == '__main__':
    aruba_app.run()