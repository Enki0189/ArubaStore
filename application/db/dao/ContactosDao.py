class ContactosDao:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def insertar_contacto(self, contacto):
        cur = self.db_connection.mysql.connection.cursor()
        cur.execute('INSERT INTO registro_usuarios (id_dni, nombre_usuario, apellido_usuario, mail_usuario, alias, contrasenia) VALUES(%s, %s, %s, %s, %s, %s)', (contacto.id_dni, contacto.nombre_usuario, contacto.apellido_usuario, contacto.mail_usuario, contacto.alias, contacto.contrasenia))
        self.db_connection.mysql.connection.commit()
    
    def obtener_contactos(self):
        cur = self.db_connection.mysql.connection.cursor()
        cur.execute('SELECT * FROM registro_usuarios')
        data = cur.fetchall()
        return data

    def obtener_contactos_por_ID(self,id):
        cur = self.db_connection.mysql.connection.cursor()
        cur.execute("SELECT * FROM registro_usuarios WHERE id_dni = %s", [id])
        data = cur.fetchall()
        return data

    def editar_contacto(self,contacto):
        cur = self.db_connection.mysql.connection.cursor()
        cur.execute("""
            UPDATE registro_usuarios
            SET nombre_usuario = %s,
                apellido_usuario = %s,
                mail_usuario = %s,
                alias = %s,
                contrasenia = %s
            WHERE id_dni = %s
        """, (contacto.nombre_usuario, contacto.apellido_usuario, contacto.mail_usuario, contacto.alias, contacto.contrasenia, contacto.id_dni))
        self.db_connection.mysql.connection.commit()

    def borrar_contacto(self,id):
        cur = self.db_connection.mysql.connection.cursor()
        cur.execute('DELETE FROM registro_usuarios WHERE id_dni = {0}'.format(id))
        self.db_connection.mysql.connection.commit()
