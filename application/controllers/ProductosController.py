from flask import flash, redirect, render_template, request, url_for

from application.db.dao.ProductosDao import ProductosDao
from application.model.Producto import Producto

class ProductosController:
    def __init__(self, app, db_connection):
        self.app = app
        self.register_routes()
        self.productos_dao = ProductosDao(db_connection)

    #Se definen endpoints de productos
    def register_routes(self):
        self.app.add_url_rule('/productos', 'productos', self.productos)
        self.app.add_url_rule('/producto', 'producto', self.producto)
        self.app.add_url_rule('/producto', 'crearProducto', self.crear_producto, methods=['POST'])
        self.app.add_url_rule('/producto/<int:id>', 'editarProducto', self.editar_producto, methods=['PUT'])
        self.app.add_url_rule('/producto/<int:id>', 'borrarProducto', self.borrar_producto, methods=['DELETE'])
        self.app.add_url_rule('/abmProducto', 'abmProducto', self.abm_producto)

    def productos(self):
        #Obtiene productos desde la base de datos
        db_products = self.productos_dao.obtener_productos()

        #Se crea un array vacio donde se van a cargar los productos en formato Json
        productos_json = []
        
        # Se itera los productos obtrenidos desde la base de datos y se agrega a cada uno de ellos en el array products.
        # Notar que cada producto tiene un metodo llamado transformar_a_json() que transforma su contenido en formato json.
        for product in db_products:
            productos_json.append(product.transformar_a_json())
        
        #Se retorna el template con los productos cargados en formato json en la variable products del template
        return render_template('productos.html', products=productos_json)

    def producto(self):
        return render_template("producto.html")
    
    def abm_producto(self):
        return render_template("abmProducto.html")

    def crear_producto(self):
        nombre_producto = request.form['nombreProducto']
        url_imagen = request.form['urlImagen']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        
        producto = Producto(None, nombre_producto, descripcion, precio, stock, url_imagen)

        try:
            self.productos_dao.insertar_producto(producto)
            flash('Producto creado exitosamente!', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            print(f"Error: {e}")
            flash('Hubo un error al crear el producto. Por favor intenta nuevamente.', 'danger')

        return redirect(url_for('abmProducto'))

    def editar_producto(self, idProducto):
        id_producto = request.form['idProducto']
        nombre_producto = request.form['nombreProducto']
        url_imagen = request.form['urlImagen']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        producto = Producto(id_producto, nombre_producto, descripcion, precio, stock, url_imagen)
        
        try:
            self.productos_dao.editar_producto(producto)
            flash('Producto actualizado exitosamente!', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            self.mysql.connection.rollback()
            print(f"Error: {e}")
            flash('Hubo un error al actualizar el producto. Por favor intenta nuevamente.', 'danger')

        return redirect(url_for('abmProducto'))

    def borrar_producto(self, id_producto):
        print('Se recibe eliminación de producto.')

        try:
            producto = Producto(id_producto, None, None, None, None, None)
            self.productos_dao.eliminar_producto(producto)
            flash('Producto eliminado exitosamente!', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            self.mysql.connection.rollback()
            print(f"Error: {e}")
            flash('Hubo un error al eliminar el producto. Por favor intenta nuevamente.', 'danger')

        return redirect(url_for('abmProducto'))
