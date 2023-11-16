from flask import flash, redirect, render_template, request, url_for, session
from application.model.Usuario import Usuario
from application.db.dao.UsuariosDao import UsuariosDao

class UsuariosController:
    def __init__(self, app, db_connection):
        self.app = app
        self.register_routes()
        self.usuarios_dao = UsuariosDao(db_connection)
    
    #Se definen endpoints de usuarios
    def register_routes(self):
        self.app.add_url_rule('/usuario', 'crearUsuario', self.crear_usuario, methods=['POST'])
        self.app.add_url_rule('/usuario/login', 'usuarioLogin', self.usuario_login, methods=['POST'])
        self.app.add_url_rule('/login', 'login', self.login)
        self.app.add_url_rule('/logout', 'logout', self.logout)
    
    def crear_usuario(self):
        print('Se recibe solicitud de creación de nuevo usuario.')
        nombre_usuario = request.form['userName']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['phone']
        direccion = request.form['address']
        provincia = request.form['province']
        personal_id = request.form['personalId']
        rol = 1
        
        nuevo_usuario = Usuario(nombre_usuario, password, nombre, apellido, email, telefono, direccion, provincia, personal_id, rol)
        
        try:
            self.usuarios_dao.insertar_usuario(nuevo_usuario)
            flash('Usuario creado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            self.mysql.connection.rollback()
            print(f"Error: {e}")
            flash('Hubo un error al crear el usuario. Por favor intenta nuevamente.', 'danger')

        return redirect(url_for('register'))

    def usuario_login(self):
        email = request.form['email']
        password = request.form['password']

        try:
            usuario = self.usuarios_dao.buscar_usuario_por_email(email)
            if usuario and usuario.password == password:  # Aquí simplemente se compara directamente, pero deberías usar hashing.
                session['logged_in'] = True
                session['user_email'] = email
                session['tipo_usuario'] = usuario.rol
                flash('Inicio de sesión correcto.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Usuario y/o contraseñas incorrectos. Por favor intenta nuevamente.', 'danger')
        except Exception as e:
            print(f"Error: {e}")
            flash('Hubo un error al intentar iniciar sesión. Por favor intenta nuevamente.', 'danger')

        return redirect(url_for('login'))
    
    def login(self):
        return render_template("login.html")

    def logout(self):
        session.pop('logged_in', None)
        session.pop('user_email', None)
        session.pop('tipo_usuario', None)
        flash('Has cerrado sesión.', 'success')
        return redirect(url_for('index'))
        