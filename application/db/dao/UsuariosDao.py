from application.model.Usuario import Usuario

class UsuariosDao:
    def __init__(self, db_connection):
        self.mysql = db_connection.mysql
        
    def insertar_usuario(self, usuario):
        cur = self.mysql.connection.cursor()
        cur.execute('INSERT INTO usuario (nombreUsuario, contraseña, rol, email, direccion, telefono, nombreYapellido, cuil, provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (usuario.nombre, usuario.password, usuario.rol, usuario.email, usuario.direccion, usuario.telefono, usuario.apellido, usuario.personal_id, usuario.provincia))
        self.mysql.connection.commit()
    
    def buscar_usuario_por_email(self, email):
        cur = self.mysql.connection.cursor()
        cur.execute('SELECT U.idUsuario, U.NombreUsuario, U.nombreYapellido, U.Contraseña, R.descripcion, U.email, U.direccion, U.telefono, U.cuil, U.provincia FROM usuario U JOIN roles R ON U.rol = R.idRoles WHERE email = %s', [email])
        user_data = cur.fetchone()
        
        user_id = user_data[0]
        nombre = user_data[1].strip()
        apellido = user_data[2]
        password = user_data[3]
        rol = user_data[4]
        email = user_data[5]
        direccion = user_data[6]
        telefono = user_data[7]
        cuil = user_data[8]
        provincia = user_data[9]
        
        usuario = Usuario(user_id, nombre, apellido, password, rol, email, direccion, telefono, cuil, provincia)
        return usuario
    
    def eliminar_usuario(self, usuario):
        cur = self.mysql.connection.cursor()
        cur.execute('DELETE FROM Usuario WHERE idUsuario = %s', usuario.id)
        self.mysql.connection.commit()