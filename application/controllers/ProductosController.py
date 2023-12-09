from flask import flash, redirect, render_template, request, url_for
from flask import session

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
        self.app.add_url_rule('/empty_cart', 'empty_cart', self.empty_cart)
        self.app.add_url_rule('/producto', 'crearProducto', self.crear_producto, methods=['POST'])
        self.app.add_url_rule('/add_to_cart', 'add_to_cart', self.add_to_cart, methods=['POST'])
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
        
        if "cart" not in session :
            session["cart"] = []
        print(session["cart"])
        if "totalprice" not in session :
            session["totalprice"] = 0
        session["productosCargados"] = productos_json 
        
        #Se retorna el template con los productos cargados en formato json en la variable products del template
        return render_template('productos.html', products=productos_json)

    def add_to_cart(self):
        item_id = int(request.form["id"])
        print(item_id)

        # Buscar el producto en session["productosCargados"] usando una función lambda
        selected_product = next((product for product in session["productosCargados"] if product["id"] == item_id), None)

        if selected_product:
            # Buscar el producto en session["cart"] usando una función lambda
            cart_product = next((product for product in session["cart"] if product["id"] == item_id), None)

            if cart_product:
                # Incrementar la propiedad "quantity" en 1 si ya existe en el carrito
                cart_product["quantity"] += 1
            else:
                # Agregar el producto al carrito con "quantity" establecido en 1
                selected_product["quantity"] = 1
                session["cart"].append(selected_product)

            product_price = selected_product["price"].replace('$', '').replace(',', '')
            session["totalprice"] = float(session["totalprice"]) + float(product_price)

        return redirect(url_for('productos'))

    def empty_cart(self):
        session["cart"] = []
        session["totalprice"] = 0
        flash('Se han eliminado todos los productos del carrito', 'success')
        return redirect(url_for("productos"))
    
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
