from flask_mysqldb import MySQL

class DBConnection:

    def __init__(self, app):
        #MySQL connection
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = '010420'
        app.config['MYSQL_DB'] = 'aruba_store'
        self.mysql = MySQL(app)
