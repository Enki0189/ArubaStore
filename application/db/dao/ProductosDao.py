from application.model.Producto import Producto

class ProductosDao:
    
    def __init__(self, db_connection):
        self.mysql = db_connection.mysql

    def insertar_producto(self, producto):
        cur = self.mysql.connection.cursor()
        cur.execute('INSERT INTO productos (NombreProducto, descripcion, precio, stock, urlImagen) VALUES (%s, %s, %s, %s, %s)', (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.imagen))
        self.mysql.connection.commit()
    
    def buscar_producto_por_nombre(self, nombre_producto):
        cur = self.mysql.connection.cursor()
        cur.execute('SELECT idProductos, NombreProducto, Descripcion, precio, stock, urlImagen FROM productos WHERE NombreProducto = %s', nombre_producto)
        product_data = cur.fetchone()
        
        if not product_data:
            return None
        
        id_producto = product_data[0]
        nombre = product_data[1].strip()
        descripcion = product_data[2].strip()
        precio = product_data[3] 
        stock = product_data[4] 
        url_imagen = product_data[5]
        print(nombre)
        print(descripcion)
        producto = Producto(id_producto, nombre, descripcion, precio, stock, url_imagen)
        
        return producto
        
    def obtener_productos(self):
        cur = self.mysql.connection.cursor()
        cur.execute('SELECT idProductos, NombreProducto, Descripcion, precio, stock, urlImagen FROM productos')
        db_products = cur.fetchall()

        products = []
        for product_data in db_products:
            id_producto = product_data[0]
            nombre = product_data[1].strip()
            descripcion = product_data[2].strip()
            precio = product_data[3] 
            stock = product_data[4] 
            url_imagen = product_data[5]
            print(nombre)
            print(descripcion)
            product = Producto(id_producto, nombre, descripcion, precio, stock, url_imagen)
            products.append(product)

        return products
    
    def editar_producto(self, producto):
        cur = self.mysql.connection.cursor()
        cur.execute('UPDATE productos SET nombreProducto = %s, descripcion = %s, precio = %s, stock = %s, urlImagen = %s WHERE idProductos = %s', (producto.nombre_producto, producto.descripcion, producto.precio, producto.stock, producto.url_imagen, producto.id))
        self.mysql.connection.commit()
    
    def eliminar_producto(self, producto):
        cur = self.mysql.connection.cursor()
        cur.execute('DELETE FROM productos WHERE idProductos = %s', producto.id)
        self.mysql.connection.commit()