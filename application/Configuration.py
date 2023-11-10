from flask import Flask
from flask_mysqldb import MySQL
from application.db.DBConnection import DBConnection

def create_app():
    app = Flask(__name__)
    app.secret_key = 'alguna_clave_secreta_y_dificil_de_adivinar'
    mysql = MySQL(app)
    db_connector = DBConnection(app)

    return app, mysql, db_connector
